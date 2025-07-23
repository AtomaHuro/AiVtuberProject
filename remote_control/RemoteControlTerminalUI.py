import requests

def main():
    print("Remote Terminal UI for AI VTuber")
    while True:
        cmd = input(">> ")
        if cmd == "exit": break
        res = requests.post("http://localhost:6543/api/control/trigger", json={"type": cmd})
        print(res.text)

if __name__ == "__main__":
    main()
