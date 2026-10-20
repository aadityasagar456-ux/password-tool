import hashlib
import requests

def check_breach(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"API se connect nahi ho paya: {e}"}

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return {"breached": True, "count": int(count)}

    return {"breached": False, "count": 0}

if __name__ == "__main__":
    pwd = input("Password enter karo: ")
    result = check_breach(pwd)
    if "error" in result:
        print(result["error"])
    elif result["breached"]:
        print(f"Ye password {result['count']:,} baar leak ho chuka hai. Isse use mat karo!")
    else:
        print("Ye password known breaches mein nahi mila.")