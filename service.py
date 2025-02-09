import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
# from main import main

import subprocess

class ServiceConfig(BaseModel):
    host: str
    port: int
    assigned: bool
    service_name: str

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        
    def read_config(self) -> Dict:
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def write_config(self, config: Dict):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_available_service(self) -> Optional[ServiceConfig]:
        config = self.read_config()
        for service in config['services']:
            if not service['assigned']:
                return ServiceConfig(**service)
        return None
    
    def mark_service_as_used(self, host: str, port: int):
        config = self.read_config()
        for service in config['services']:
            if service['host'] == host and service['port'] == port:
                service['assigned'] = True
                break
        self.write_config(config)
    
    def release_service(self, host: str, port: int):
        config = self.read_config()
        for service in config['services']:
            if service['host'] == host and service['port'] == port:
                service['assigned'] = False
                break
        self.write_config(config)

class InputModel(BaseModel):
    data: Dict[str, Any]

# Initialize FastAPI app with config management
# config_path = os.path.join(os.path.dirname(__file__), "service_config.json")
# config_manager = ConfigManager(config_path)
# service_config = config_manager.get_available_service()

# if not service_config:
#     raise Exception("No available service configurations found")

app = FastAPI()

@app.post("/run")
async def run_main(input_data: InputModel):
    try:
        # Execute the command and capture both stdout and stderr
        # result1 = subprocess.run(["uv", "lock"], capture_output=True, text=True)
        # print(result1)
        # result2 = subprocess.run(["uv", "lock"], capture_output=True, text=True)
        # print(result2)
        # subprocess.run
        result = subprocess.run(
            'crewai run', shell=True, capture_output=True, text=True
        )
        
        # Save stdout to a file
        output_file = "command_output.txt"
        with open(output_file, "w") as file:
            file.write(result.stdout)
        
        # Save stderr (errors) to a separate file, if any
        error_file = "command_errors.txt"
        if result.stderr:
            with open(error_file, "w") as file:
                file.write(result.stderr)
        
        # Print messages for logging purposes
        print(f"Command output saved to {output_file}")
        if result.stderr:
            print(f"Command errors saved to {error_file}")
        
        # Return status, stdout, and stderr in the API response
        return {
            "status": "success" if result.returncode == 0 else "failure",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service_name": service_config.service_name,
        "host": service_config.host,
        "port": service_config.port
    }



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app
    )
