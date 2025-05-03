from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import sys
import inspect
import subprocess
import tempfile
import os
import logging
from src.healer import execute_self_healing_code_system

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def code_editor(request):
    return render(request, "web/code_editor.html")


def execute_python_code(function_code, arguments):
    try:
        logger.debug(f"Executing Python code: {function_code}")
        logger.debug(f"With arguments: {arguments}")

        namespace = {}
        try:
            exec(function_code, namespace)
        except Exception as e:
            return f"Error: Failed to execute function code - {str(e)}"

        try:
            tree = ast.parse(function_code)
            if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
                return "Error: No function definition found in code"
            function_name = tree.body[0].name
            logger.debug(f"Found function name: {function_name}")
        except Exception as e:
            return f"Error: Failed to parse function code - {str(e)}"

        try:
            function = namespace.get(function_name)
            if function is None:
                return f"Error: Function '{function_name}' not found"
            logger.debug(f"Retrieved function object: {function}")
        except Exception as e:
            return f"Error: Failed to get function object - {str(e)}"

        try:
            args_dict = json.loads(arguments)
            logger.debug(f"Parsed arguments: {args_dict}")

            # Convert sequential arguments to tuple
            args = tuple(args_dict[f"arg{i+1}"] for i in range(len(args_dict)))
            logger.debug(f"Converted arguments to tuple: {args}")
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format - {str(e)}"
        except KeyError as e:
            return f"Error: Missing argument {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

        try:
            result = execute_self_healing_code_system(function, args)
            logger.debug(f"Execution result: {result}")
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def execute_javascript_code(function_code, arguments, language="javascript"):
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".ts" if language == "typescript" else ".js", delete=False
        ) as temp:
            if language == "typescript":
                program = f"""
{function_code}

const args = {arguments};
console.log(JSON.stringify(exampleFunction(args.arg1, args.arg2)));
"""
            else:
                program = f"""
{function_code}

const args = {arguments};
console.log(JSON.stringify(exampleFunction(args.arg1, args.arg2)));
"""
            temp.write(program.encode())
            temp_path = temp.name

        try:
            if language == "typescript":
                # First compile TypeScript to JavaScript
                compile_result = subprocess.run(
                    ["tsc", temp_path, "--outFile", f"{temp_path}.js"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                if compile_result.returncode != 0:
                    return f"TypeScript compilation error: {compile_result.stderr}"

                # Then run the compiled JavaScript
                result = subprocess.run(
                    ["node", f"{temp_path}.js"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
            else:
                result = subprocess.run(
                    ["node", temp_path], capture_output=True, text=True, check=True
                )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
        finally:
            os.unlink(temp_path)
            if language == "typescript" and os.path.exists(f"{temp_path}.js"):
                os.unlink(f"{temp_path}.js")
    except Exception as e:
        return f"Error: {str(e)}"


def execute_c_code(function_code, arguments):
    try:
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp:
            args_dict = json.loads(arguments)
            program = f"""
#include <stdio.h>
#include <stdlib.h>

{function_code}

int main() {{
    int x = {args_dict['arg1']};
    int y = {args_dict['arg2']};
    int result = example_function(x, y);
    printf("%d\\n", result);
    return 0;
}}
"""
            temp.write(program.encode())
            temp_path = temp.name

        try:
            compile_result = subprocess.run(
                ["gcc", temp_path, "-o", f"{temp_path}.out"],
                capture_output=True,
                text=True,
                check=True,
            )

            if compile_result.returncode == 0:
                result = subprocess.run(
                    [f"{temp_path}.out"], capture_output=True, text=True, check=True
                )
                return result.stdout.strip()
            else:
                return f"Compilation Error: {compile_result.stderr}"
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            if os.path.exists(f"{temp_path}.out"):
                os.unlink(f"{temp_path}.out")
    except Exception as e:
        return f"Error: {str(e)}"


@csrf_exempt
def execute_code(request):
    if request.method == "POST":
        try:
            logger.debug(f"Received request body: {request.body}")

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse(
                    {"status": "error", "error": f"Invalid JSON in request: {str(e)}"},
                    status=400,
                )

            function_code = data.get("function_code")
            arguments = data.get("arguments")
            language = data.get("language", "python")

            logger.debug(f"Parsed data - Language: {language}")
            logger.debug(f"Function code: {function_code}")
            logger.debug(f"Arguments: {arguments}")

            if not function_code:
                return JsonResponse(
                    {"status": "error", "error": "Missing function code"}, status=400
                )
            if not arguments:
                return JsonResponse(
                    {"status": "error", "error": "Missing arguments"}, status=400
                )

            try:
                if language == "python":
                    result = execute_python_code(function_code, arguments)
                elif language in ["javascript", "typescript"]:
                    result = execute_javascript_code(function_code, arguments, language)
                elif language == "clike":
                    result = execute_c_code(function_code, arguments)
                else:
                    return JsonResponse(
                        {
                            "status": "error",
                            "error": f"Unsupported language: {language}",
                        },
                        status=400,
                    )

                logger.debug(f"Execution result: {result}")

                return JsonResponse({"status": "success", "result": str(result)})
            except Exception as e:
                return JsonResponse(
                    {"status": "error", "error": f"Execution error: {str(e)}"},
                    status=500,
                )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "error": f"Server error: {str(e)}"}, status=500
            )
    return JsonResponse(
        {"status": "error", "error": "Invalid request method"}, status=405
    )
