from django.shortcuts import render
from django.http import JsonResponse
from .backend.cnc_to_opcua import MongoToOPCUAHandler, MySQLToOPCUAHandler
from .backend.display_data import CNCDataFetcher
from opcua import Client
from threading import Thread
from pymongo import MongoClient
import mysql.connector

# OPC UA client setup
opcua_client = Client("opc.tcp://DESKTOP-DLRKACU:53530/OPCUA/SimulationServer")

def connect_opcua_client():
    try:
        opcua_client.connect()
        print(" OPC UA client connected for data display")
    except Exception as e:
        print(f"OPC UA connection error: {e}")

connect_opcua_client()

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["CNC_DATA"]
collection = db["Machine_status"]

# Handlers
opc_handler = MongoToOPCUAHandler()
mysql_handler = MySQLToOPCUAHandler()
opcua_thread = None
mysql_thread = None
display_data_active = False
active_data_source = None

# Page Views
def index(request): return render(request, 'Home/index.html')
def Contacts(request): return render(request, 'Home/Contacts.html')
def About_us(request): return render(request, 'Home/About_us.html')
def OPC_UA(request): return render(request, 'Home/OPC_UA.html')

# MongoDB transfer controls
def start_transfer(request):
    global opcua_thread, active_data_source
    try:
        if not opcua_thread or not opcua_thread.is_alive():
            opcua_thread = Thread(target=opc_handler.start)
            opcua_thread.daemon = True
            opcua_thread.start()
            active_data_source = "MongoDB"
            print("Started MongoDB → OPC UA transfer")
            return JsonResponse({'status': 'Data transfer started from MongoDB'})
        return JsonResponse({'status': 'MongoDB transfer already running'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})

def stop_transfer(request):
    global active_data_source
    try:
        opc_handler.stop()
        active_data_source = None
        print(" MongoDB transfer stopped")
        return JsonResponse({'status': 'Data transfer stopped'})
    except Exception as e:
        return JsonResponse({'status': 'Error during stop', 'message': str(e)})

# MySQL transfer controls
def start_mysql_transfer(request):
    global mysql_thread, active_data_source
    try:
        if not mysql_thread or not mysql_thread.is_alive():
            mysql_thread = Thread(target=mysql_handler.start)
            mysql_thread.daemon = True
            mysql_thread.start()
            active_data_source = "MySQL"
            print(" Started MySQL → OPC UA transfer")
            return JsonResponse({'status': 'Data transfer started from MySQL'})
        return JsonResponse({'status': 'MySQL transfer already running'})
    except Exception as e:
        return JsonResponse({'status': 'Error', 'message': str(e)})

def stop_mysql_transfer(request):
    global active_data_source
    try:
        mysql_handler.stop()
        active_data_source = None
        print(" MySQL transfer stopped")
        return JsonResponse({'status': 'MySQL data transfer stopped'})
    except Exception as e:
        return JsonResponse({'status': 'Error during MySQL stop', 'message': str(e)})

# Show live OPC UA data (no filtering)
def show_data(request):
    global display_data_active, active_data_source
    try:
        display_data_active = True
        fetcher = CNCDataFetcher(opcua_client)
        data = fetcher.get_data()

        if "Error" in data:
            return JsonResponse({'error': data["Error"]})

        return JsonResponse({
            'source': active_data_source or "Unknown",
            'data': data
        })

    except Exception as e:
        return JsonResponse({'error': str(e)})

# Hide live data flag (optional logic)
def hide_data(request):
    global display_data_active
    display_data_active = False
    return JsonResponse({'status': 'Data hidden'})

# ✅ Filtered live OPC UA data based on status
def filtered_data(request):
    global active_data_source
    try:
        status_filter = request.GET.get("status")  # e.g., ?status=Idle

        fetcher = CNCDataFetcher(opcua_client)
        all_data = fetcher.get_data()

        if "Error" in all_data:
            return JsonResponse({"error": all_data["Error"]})

        if status_filter and status_filter.lower() != "all":
            filtered = [entry for entry in all_data if entry.get("status") == status_filter]
        else:
            filtered = all_data

        return JsonResponse({
            "status": "ok",
            "source": active_data_source or "Unknown",
            "data": filtered
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
