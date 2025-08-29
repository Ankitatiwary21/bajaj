import requests

URL = "http://127.0.0.1:5000/bfhl"

def hit(payload):
    print("Request:", payload)
    r = requests.post(URL, json=payload)
    print("Status:", r.status_code)
    print("Response:", r.json())
    print("-" * 60)

# Example A
hit({"data": ["a", "1", "334", "4", "R", "$"]})
# Expected:
# odd: ["1"], even: ["334","4"], alphabets: ["A","R"], specials: ["$"], sum: "339", concat: "Ra"

# Example B
hit({"data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]})
# Expected:
# odd: ["5"], even: ["2","4","92"], alphabets: ["A","Y","B"], specials: ["&","-","*"], sum: "103", concat: "ByA"

# Example C
hit({"data": ["A", "ABcD", "DOE"]})
# Expected:
# odd: [], even: [], alphabets: ["A","ABCD","DOE"], specials: [], sum: "0", concat: "EoDdCbAa"
