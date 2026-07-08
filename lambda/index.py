import json
import urllib.request

def lambda_handler(event, context):
    url = "http://localhost:2772/applications/AiGateway/environments/Prod/configurations/ModelRouter"
    
    try:
        response = urllib.request.urlopen(url)
        config = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": f"Failed to fetch AppConfig: {str(e)}"})}

    body = json.loads(event.get("body", "{}")) if event.get("body") else {}
    user_prompt = body.get("prompt", "")

    max_tokens = config.get("max_input_tokens_allowed", 1000)
    if len(user_prompt.split()) > max_tokens:
        return {
            "statusCode": 400, 
            "body": json.dumps({"error": f"Prompt exceeds safe limits of {max_tokens} words."})
        }

    selected_model = config.get("active_llm_model", "gpt-4o-mini")
    prompt_version = config.get("system_prompt_version", "v1.0")

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "status": "success",
            "model_used": selected_model,
            "prompt_version": prompt_version,
            "ai_response": f"[Mocked LLM Response] Processed using model: {selected_model}"
        })
    }
