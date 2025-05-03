from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import sys
import inspect
from src.healer import execute_self_healing_code_system


def code_editor(request):
    return render(request, "web/code_editor.html")


@csrf_exempt
def execute_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            function_code = data.get("function_code")
            arguments = data.get("arguments")

            # Create a namespace and execute the function code
            namespace = {}
            exec(function_code, namespace)

            # Get the function name from the code
            tree = ast.parse(function_code)
            function_name = tree.body[0].name

            # Get the function object
            function = namespace[function_name]

            # Parse arguments
            args = ast.literal_eval(arguments)

            # Execute the function with self-healing
            result = execute_self_healing_code_system(function, args)

            return JsonResponse({"status": "success", "result": str(result)})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=400)
    return JsonResponse(
        {"status": "error", "error": "Invalid request method"}, status=405
    )
