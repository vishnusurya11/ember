import websocket
import uuid
import json
import urllib.request
import urllib.parse
import datetime
import random
from PIL import Image
import io


class ImageGenerator:
    def __init__(self, server_address, workflow_file):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())
        self.workflow_file = workflow_file

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode("utf-8")
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt", data=data)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())

    def get_image(self, filename, subfolder, folder_type):
        data = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(
            f"http://{self.server_address}/view?{url_values}"
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            f"http://{self.server_address}/history/{prompt_id}"
        ) as response:
            return json.loads(response.read())

    def get_images(self, ws, prompt):
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        current_node = ""

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message["type"] == "executing":
                    data = message["data"]
                    if data["prompt_id"] == prompt_id:
                        if data["node"] is None:
                            break  # Execution is done
                        else:
                            current_node = data["node"]
            else:
                if current_node == "save_image_websocket_node":
                    images_output = output_images.get(current_node, [])
                    images_output.append(out[8:])
                    output_images[current_node] = images_output

        return output_images

    def load_workflow(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.loads(f.read())

    def save_images(self, images, save_dir):
        for node_id, image_datas in images.items():
            for image_data in image_datas:
                image = Image.open(io.BytesIO(image_data))
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y%m%d%H%M%S")
                image.save(f"{save_dir}/{node_id}_{timestamp}.png")

    def update_prompt(self, prompt, updates):
        for node_id, params in updates.items():
            if node_id in prompt:
                for key, value in params.items():
                    prompt[node_id]["inputs"][key] = value

    def generate_images(self, save_dir, updates=None):
        # Load workflow
        prompt = self.load_workflow(self.workflow_file)

        # Apply updates
        if updates:
            self.update_prompt(prompt, updates)

        # Connect to WebSocket and get images
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")

        try:
            print("Triggering the UI")
            images = self.get_images(ws, prompt)
            print("Images generated")
            self.save_images(images, save_dir)
            print("Images saved")
        finally:
            ws.close()


def main():
    # Configuration
    SERVER_ADDRESS = "127.0.0.1:8188"
    WORKFLOW_FILE = "Imtovid_workflow.json"
    SAVE_DIR = "E:/ComfyUI_windows_portable/apiplay"

    generator = ImageGenerator(SERVER_ADDRESS, WORKFLOW_FILE)

    # Example parameters for experimentation
    seed = random.randint(1, 1000000000)
    updates = {
        "3": {"seed": seed, "steps": 40, "cfg": 3.0},
        "59": {"image": "E:/ComfyUI_windows_portable/apiplay/im4.png"},
    }

    generator.generate_images(SAVE_DIR, updates=updates)


if __name__ == "__main__":
    main()
