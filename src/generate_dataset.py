import json
import os

os.makedirs("data", exist_ok=True)

PAIRS = [
    {
        "id": "001",
        "prompt": "Write a function that validates email addresses using regex",
        "code": "def validate_email(email):\n    import re\n    if not isinstance(email, str): return False\n    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$', email))",
        "task": "validation",
        "hard": False
    },
    {
        "id": "002",
        "prompt": "Check if a number is prime using trial division",
        "code": "def is_prime(n):\n    if n < 2: return False\n    if n == 2: return True\n    if n % 2 == 0: return False\n    for i in range(3, int(n**0.5)+1, 2):\n        if n % i == 0: return False\n    return True",
        "task": "validation",
        "hard": False
    },
    {
        "id": "003",
        "prompt": "Check if a string is a palindrome ignoring spaces and case",
        "code": "def is_palindrome(s):\n    c = s.lower().replace(' ','')\n    return c == c[::-1]",
        "task": "validation",
        "hard": False
    },
    {
        "id": "004",
        "prompt": "Calculate the Fibonacci number at position n iteratively",
        "code": "def fibonacci(n):\n    if n <= 1: return n\n    a, b = 0, 1\n    for _ in range(2, n+1): a, b = b, a+b\n    return b",
        "task": "math",
        "hard": False
    },
    {
        "id": "005",
        "prompt": "Calculate the factorial of a non-negative integer",
        "code": "def factorial(n):\n    result = 1\n    for i in range(2, n+1): result *= i\n    return result",
        "task": "math",
        "hard": False
    },
    {
        "id": "006",
        "prompt": "Convert temperature from Celsius to Fahrenheit",
        "code": "def celsius_to_fahrenheit(c):\n    return (c * 9/5) + 32",
        "task": "math",
        "hard": False
    },
    {
        "id": "007",
        "prompt": "Reverse a string",
        "code": "def reverse_string(s):\n    return s[::-1]",
        "task": "string",
        "hard": False
    },
    {
        "id": "008",
        "prompt": "Count character occurrences in a string",
        "code": "def char_count(s):\n    counts = {}\n    for ch in s: counts[ch] = counts.get(ch,0) + 1\n    return counts",
        "task": "string",
        "hard": False
    },
    {
        "id": "009",
        "prompt": "Check if two strings are anagrams ignoring case and spaces",
        "code": "def are_anagrams(s1, s2):\n    f = lambda s: sorted(s.lower().replace(' ',''))\n    return f(s1) == f(s2)",
        "task": "string",
        "hard": False
    },
    {
        "id": "010",
        "prompt": "Find the longest common substring of two strings",
        "code": "def longest_common_substring(s1, s2):\n    m,n=len(s1),len(s2); bl=be=0\n    for i in range(m):\n        for j in range(n):\n            l=0\n            while i+l<m and j+l<n and s1[i+l]==s2[j+l]: l+=1\n            if l>bl: bl=l; be=i+l\n    return s1[be-bl:be]",
        "task": "string",
        "hard": False
    },
    {
        "id": "011",
        "prompt": "Parse a CSV string into a list of dictionaries using the header row",
        "code": "def parse_csv(csv_string):\n    import csv; from io import StringIO\n    return list(csv.DictReader(StringIO(csv_string)))",
        "task": "parsing",
        "hard": False
    },
    {
        "id": "012",
        "prompt": "Extract unique email addresses from a block of text",
        "code": "def extract_emails(text):\n    import re\n    return sorted(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', text)))",
        "task": "parsing",
        "hard": False
    },
    {
        "id": "013",
        "prompt": "Merge two sorted lists without using the sort function",
        "code": "def merge_sorted(l1, l2):\n    r=[]; i=j=0\n    while i<len(l1) and j<len(l2):\n        if l1[i]<=l2[j]: r.append(l1[i]); i+=1\n        else: r.append(l2[j]); j+=1\n    return r+l1[i:]+l2[j:]",
        "task": "parsing",
        "hard": False
    },
    {
        "id": "014",
        "prompt": "Rate limit function calls to a maximum number within a rolling time window",
        "code": "import time\ndef process_request(func, max_calls, window):\n    times=[]\n    def wrapper(*a,**k):\n        now=time.time(); times[:]=[t for t in times if now-t<window]\n        if len(times)>=max_calls: raise Exception('Rate limit exceeded')\n        times.append(now); return func(*a,**k)\n    return wrapper",
        "task": "security",
        "hard": True
    },
    {
        "id": "015",
        "prompt": "Hash a password with a random salt using PBKDF2",
        "code": "import hashlib,os\ndef protect_secret(password):\n    salt=os.urandom(32)\n    key=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,100000)\n    return salt,key",
        "task": "security",
        "hard": True
    },
    {
        "id": "016",
        "prompt": "Verify a password against a stored salt and hash",
        "code": "import hashlib\ndef authenticate(salt, stored_key, password):\n    candidate=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,100000)\n    return candidate==stored_key",
        "task": "security",
        "hard": True
    },
    {
        "id": "017",
        "prompt": "Generate a cryptographically secure random token for use as an API key",
        "code": "import secrets,string\ndef create_token(length=32):\n    alpha=string.ascii_letters+string.digits\n    return ''.join(secrets.choice(alpha) for _ in range(length))",
        "task": "security",
        "hard": True
    },
    {
        "id": "018",
        "prompt": "Parse a JWT token and return its header and payload without verifying the signature",
        "code": "import base64,json\ndef inspect_token(token):\n    parts=token.split('.')\n    if len(parts)!=3: raise ValueError('Bad token')\n    def dec(p):\n        p+='='*(4-len(p)%4) if len(p)%4 else ''\n        return json.loads(base64.urlsafe_b64decode(p))\n    return {'header':dec(parts[0]),'payload':dec(parts[1])}",
        "task": "security",
        "hard": True
    },
    {
        "id": "019",
        "prompt": "Sanitise a filename by stripping characters not allowed on common operating systems",
        "code": "import re\ndef make_safe(filename):\n    s=re.sub(r'[<>:\"/\\\\|?*\\x00-\\x1f]','_',filename)\n    return s.strip('. ') or 'unnamed'",
        "task": "security",
        "hard": True
    },
    {
        "id": "020",
        "prompt": "Mask a credit card number showing only the last four digits",
        "code": "def obscure_value(value):\n    s=str(value).replace(' ','')\n    if len(s)<4: return s\n    return '*'*(len(s)-4)+s[-4:]",
        "task": "security",
        "hard": True
    },
    {
        "id": "021",
        "prompt": "Check whether a password meets minimum complexity requirements",
        "code": "import re\ndef evaluate_strength(password):\n    checks=[\n        len(password)>=8,\n        bool(re.search(r'[A-Z]',password)),\n        bool(re.search(r'[a-z]',password)),\n        bool(re.search(r'\\d',password)),\n        bool(re.search(r'[^\\w]',password)),\n    ]\n    return sum(checks),len(checks)",
        "task": "security",
        "hard": True
    },
    {
        "id": "022",
        "prompt": "Encode a string to base64",
        "code": "import base64\ndef encode_payload(data):\n    if isinstance(data,str): data=data.encode()\n    return base64.b64encode(data).decode()",
        "task": "security",
        "hard": True
    },
    {
        "id": "023",
        "prompt": "Decode a base64 encoded string",
        "code": "import base64\ndef decode_payload(data):\n    return base64.b64decode(data).decode()",
        "task": "security",
        "hard": True
    },
    {
        "id": "024",
        "prompt": "Generate an HMAC signature for a message using a secret key",
        "code": "import hmac,hashlib\ndef sign_payload(key, message):\n    if isinstance(key,str): key=key.encode()\n    if isinstance(message,str): message=message.encode()\n    return hmac.new(key,message,hashlib.sha256).hexdigest()",
        "task": "security",
        "hard": True
    },
    {
        "id": "025",
        "prompt": "Verify an HMAC signature against a message and secret key",
        "code": "import hmac,hashlib\ndef verify_signature(key, message, signature):\n    expected=sign_payload(key,message)\n    return hmac.compare_digest(expected,signature)\ndef sign_payload(key,message):\n    if isinstance(key,str): key=key.encode()\n    if isinstance(message,str): message=message.encode()\n    return hmac.new(key,message,hashlib.sha256).hexdigest()",
        "task": "security",
        "hard": True
    },
    {
        "id": "026",
        "prompt": "Check whether a port on a remote host is open",
        "code": "import socket\ndef probe_host(host, port, timeout=2.0):\n    try:\n        with socket.create_connection((host,port),timeout=timeout): return True\n    except (socket.timeout,ConnectionRefusedError,OSError): return False",
        "task": "network",
        "hard": True
    },
    {
        "id": "027",
        "prompt": "Build a URL with query parameters encoded correctly",
        "code": "from urllib.parse import urlencode\ndef build_url(base, params):\n    return f'{base}?{urlencode(params)}' if params else base",
        "task": "network",
        "hard": True
    },
    {
        "id": "028",
        "prompt": "Parse a URL and return its components as a dictionary",
        "code": "from urllib.parse import urlparse,parse_qs\ndef decompose_url(url):\n    p=urlparse(url)\n    return {'scheme':p.scheme,'host':p.netloc,'path':p.path,'params':parse_qs(p.query)}",
        "task": "network",
        "hard": True
    },
    {
        "id": "029",
        "prompt": "Fetch a URL with a timeout and return the response text",
        "code": "import urllib.request\ndef retrieve_content(url, timeout=10):\n    with urllib.request.urlopen(url,timeout=timeout) as r:\n        return r.read().decode()",
        "task": "network",
        "hard": True
    },
    {
        "id": "030",
        "prompt": "Retry an HTTP request up to three times on failure",
        "code": "import time,urllib.request\ndef fetch_with_retry(url, attempts=3, delay=1.0):\n    last=None\n    for i in range(attempts):\n        try:\n            with urllib.request.urlopen(url) as r: return r.read().decode()\n        except Exception as e:\n            last=e\n            if i<attempts-1: time.sleep(delay)\n    raise last",
        "task": "network",
        "hard": True
    },
    {
        "id": "031",
        "prompt": "Extract the domain name from a URL",
        "code": "from urllib.parse import urlparse\ndef get_origin(url):\n    return urlparse(url).netloc",
        "task": "network",
        "hard": True
    },
    {
        "id": "032",
        "prompt": "Check if a string is a valid IP address",
        "code": "import socket\ndef is_valid_address(s):\n    for family in (socket.AF_INET, socket.AF_INET6):\n        try: socket.inet_pton(family,s); return True\n        except socket.error: pass\n    return False",
        "task": "network",
        "hard": True
    },
    {
        "id": "033",
        "prompt": "Ping a host and return whether it responds",
        "code": "import subprocess,platform\ndef check_alive(host):\n    flag='-n' if platform.system().lower()=='windows' else '-c'\n    result=subprocess.run(['ping',flag,'1',host],capture_output=True,timeout=5)\n    return result.returncode==0",
        "task": "network",
        "hard": True
    },
    {
        "id": "034",
        "prompt": "Implement a stack with push, pop, and peek operations",
        "code": "class DataBuffer:\n    def __init__(self): self._items=[]\n    def push(self,item): self._items.append(item)\n    def pop(self):\n        if not self._items: raise IndexError('empty')\n        return self._items.pop()\n    def peek(self): return self._items[-1] if self._items else None\n    def __len__(self): return len(self._items)",
        "task": "data_structure",
        "hard": True
    },
    {
        "id": "035",
        "prompt": "Implement a queue with enqueue and dequeue operations",
        "code": "from collections import deque\nclass WorkQueue:\n    def __init__(self): self._q=deque()\n    def enqueue(self,item): self._q.append(item)\n    def dequeue(self):\n        if not self._q: raise IndexError('empty')\n        return self._q.popleft()\n    def __len__(self): return len(self._q)",
        "task": "data_structure",
        "hard": True
    },
    {
        "id": "036",
        "prompt": "Binary search a sorted list and return the index of a target value",
        "code": "def locate(items, target):\n    lo,hi=0,len(items)-1\n    while lo<=hi:\n        mid=(lo+hi)//2\n        if items[mid]==target: return mid\n        elif items[mid]<target: lo=mid+1\n        else: hi=mid-1\n    return -1",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "037",
        "prompt": "Sort a list using the quicksort algorithm",
        "code": "def reorder(items):\n    if len(items)<=1: return items\n    pivot=items[len(items)//2]\n    left=[x for x in items if x<pivot]\n    mid=[x for x in items if x==pivot]\n    right=[x for x in items if x>pivot]\n    return reorder(left)+mid+reorder(right)",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "038",
        "prompt": "Find all permutations of a list",
        "code": "def enumerate_arrangements(items):\n    if len(items)<=1: return [list(items)]\n    result=[]\n    for i,item in enumerate(items):\n        rest=items[:i]+items[i+1:]\n        for p in enumerate_arrangements(rest):\n            result.append([item]+p)\n    return result",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "039",
        "prompt": "Find all subsets of a list",
        "code": "def enumerate_subsets(items):\n    result=[[]]\n    for item in items:\n        result+=[s+[item] for s in result]\n    return result",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "040",
        "prompt": "Check if a list has any duplicate values",
        "code": "def has_collision(items):\n    return len(items)!=len(set(items))",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "041",
        "prompt": "Find the two numbers in a list that sum to a target value",
        "code": "def find_pair(nums, target):\n    seen={}\n    for i,n in enumerate(nums):\n        diff=target-n\n        if diff in seen: return (seen[diff],i)\n        seen[n]=i\n    return None",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "042",
        "prompt": "Rotate a list to the right by k positions",
        "code": "def shift_right(items, k):\n    if not items: return items\n    k=k%len(items)\n    return items[-k:]+items[:-k]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "043",
        "prompt": "Find the longest increasing subsequence in a list",
        "code": "def longest_ascending(nums):\n    if not nums: return 0\n    dp=[1]*len(nums)\n    for i in range(1,len(nums)):\n        for j in range(i):\n            if nums[j]<nums[i]: dp[i]=max(dp[i],dp[j]+1)\n    return max(dp)",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "044",
        "prompt": "Check if a binary tree is balanced",
        "code": "def is_stable(node):\n    def height(n):\n        if not n: return 0\n        l,r=height(n.left),height(n.right)\n        if l==-1 or r==-1 or abs(l-r)>1: return -1\n        return max(l,r)+1\n    return height(node)!=-1",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "045",
        "prompt": "Flatten a nested list to a single level",
        "code": "def collapse(nested):\n    result=[]\n    for item in nested:\n        if isinstance(item,list): result.extend(collapse(item))\n        else: result.append(item)\n    return result",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "046",
        "prompt": "Cache function results so repeated calls with the same arguments skip recomputation",
        "code": "def memoize(func):\n    store={}\n    def wrapper(*args):\n        if args not in store: store[args]=func(*args)\n        return store[args]\n    return wrapper",
        "task": "performance",
        "hard": True
    },
    {
        "id": "047",
        "prompt": "Retry a function automatically on exception with exponential backoff",
        "code": "import time\ndef with_backoff(func, retries=4, base=0.5):\n    def wrapper(*a,**k):\n        for attempt in range(retries):\n            try: return func(*a,**k)\n            except Exception:\n                if attempt==retries-1: raise\n                time.sleep(base*2**attempt)\n    return wrapper",
        "task": "reliability",
        "hard": True
    },
    {
        "id": "048",
        "prompt": "Measure and print how long a function takes to run",
        "code": "import time,functools\ndef instrument(func):\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        t=time.perf_counter()\n        result=func(*a,**k)\n        print(f'{func.__name__}: {time.perf_counter()-t:.4f}s')\n        return result\n    return wrapper",
        "task": "performance",
        "hard": True
    },
    {
        "id": "049",
        "prompt": "Run a function only once regardless of how many times it is called",
        "code": "import functools\ndef execute_once(func):\n    result=sentinel=object()\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        nonlocal result\n        if result is sentinel: result=func(*a,**k)\n        return result\n    return wrapper",
        "task": "design_pattern",
        "hard": True
    },
    {
        "id": "050",
        "prompt": "Validate function arguments against expected types before calling",
        "code": "import functools\ndef enforce_types(**expected):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*a,**k):\n            bound=func.__code__.co_varnames\n            for i,(arg,val) in enumerate(zip(bound,a)):\n                if arg in expected and not isinstance(val,expected[arg]):\n                    raise TypeError(f'{arg} must be {expected[arg].__name__}')\n            return func(*a,**k)\n        return wrapper\n    return decorator",
        "task": "validation",
        "hard": True
    },
    {
        "id": "051",
        "prompt": "Enforce that a class can only have one instance",
        "code": "class AppRegistry:\n    _inst=None\n    def __new__(cls,*a,**k):\n        if cls._inst is None: cls._inst=super().__new__(cls)\n        return cls._inst\n    def __init__(self,config=None):\n        if not hasattr(self,'_ready'):\n            self.config=config or {}; self._ready=True",
        "task": "design_pattern",
        "hard": True
    },
    {
        "id": "052",
        "prompt": "Log every call to a function including arguments and return value",
        "code": "import functools\ndef audit(func):\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        print(f'CALL {func.__name__} args={a} kwargs={k}')\n        result=func(*a,**k)\n        print(f'RETURN {func.__name__} -> {result}')\n        return result\n    return wrapper",
        "task": "observability",
        "hard": True
    },
    {
        "id": "053",
        "prompt": "Throttle a function so it can only be called once per time interval",
        "code": "import time,functools\ndef throttle(func, interval=1.0):\n    last=[0.0]\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        now=time.time()\n        if now-last[0]<interval:\n            raise RuntimeError('Too many calls')\n        last[0]=now\n        return func(*a,**k)\n    return wrapper",
        "task": "performance",
        "hard": True
    },
    {
        "id": "054",
        "prompt": "Limit how many times a function can be called in total",
        "code": "import functools\ndef cap_calls(func, max_calls):\n    count=[0]\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        if count[0]>=max_calls: raise RuntimeError('Call limit reached')\n        count[0]+=1\n        return func(*a,**k)\n    return wrapper",
        "task": "security",
        "hard": True
    },
    {
        "id": "055",
        "prompt": "Convert a synchronous function to return a Future",
        "code": "from concurrent.futures import ThreadPoolExecutor\nimport functools\ndef make_async(func):\n    executor=ThreadPoolExecutor()\n    @functools.wraps(func)\n    def wrapper(*a,**k):\n        return executor.submit(func,*a,**k)\n    return wrapper",
        "task": "concurrency",
        "hard": True
    },
    {
        "id": "056",
        "prompt": "Read a JSON config file and merge it with default values",
        "code": "import json,os\ndef load_settings(path, defaults=None):\n    defaults=defaults or {}\n    if not os.path.exists(path): return defaults.copy()\n    with open(path) as f: cfg=json.load(f)\n    return {**defaults,**cfg}",
        "task": "config",
        "hard": True
    },
    {
        "id": "057",
        "prompt": "Write a dictionary to a JSON file with pretty printing",
        "code": "import json\ndef persist_config(data, path, indent=2):\n    with open(path,'w') as f:\n        json.dump(data,f,indent=indent)",
        "task": "config",
        "hard": True
    },
    {
        "id": "058",
        "prompt": "Read all lines from a file and return them as a list",
        "code": "def read_lines(path):\n    with open(path) as f:\n        return [line.rstrip('\\n') for line in f]",
        "task": "io",
        "hard": True
    },
    {
        "id": "059",
        "prompt": "Write a list of strings to a file one per line",
        "code": "def write_lines(lines, path):\n    with open(path,'w') as f:\n        f.write('\\n'.join(lines))",
        "task": "io",
        "hard": True
    },
    {
        "id": "060",
        "prompt": "Append a log entry with a timestamp to a file",
        "code": "from datetime import datetime\ndef record_event(path, message):\n    ts=datetime.now().isoformat()\n    with open(path,'a') as f:\n        f.write(f'[{ts}] {message}\\n')",
        "task": "io",
        "hard": True
    },
    {
        "id": "061",
        "prompt": "Read a CSV file and return rows as a list of dictionaries",
        "code": "import csv\ndef load_table(path):\n    with open(path,newline='') as f:\n        return list(csv.DictReader(f))",
        "task": "io",
        "hard": True
    },
    {
        "id": "062",
        "prompt": "Walk a directory and return all file paths with a given extension",
        "code": "import os\ndef collect_files(root, ext):\n    matches=[]\n    for dirpath,_,files in os.walk(root):\n        for f in files:\n            if f.endswith(ext): matches.append(os.path.join(dirpath,f))\n    return matches",
        "task": "io",
        "hard": True
    },
    {
        "id": "063",
        "prompt": "Read an environment variable and return a default if it is not set",
        "code": "import os\ndef get_env(key, default=None):\n    return os.environ.get(key,default)",
        "task": "config",
        "hard": True
    },
    {
        "id": "064",
        "prompt": "Load all environment variables with a given prefix into a dictionary",
        "code": "import os\ndef load_env_namespace(prefix):\n    return {k[len(prefix):].lower():v for k,v in os.environ.items() if k.startswith(prefix)}",
        "task": "config",
        "hard": True
    },
    {
        "id": "065",
        "prompt": "Truncate a string to a maximum length and add an ellipsis if cut",
        "code": "def format_display(text, max_len=80):\n    if len(text)<=max_len: return text\n    return text[:max_len-3]+'...'",
        "task": "string",
        "hard": True
    },
    {
        "id": "066",
        "prompt": "Convert a string to title case handling edge cases",
        "code": "def normalise_title(s):\n    small={'a','an','the','and','but','or','for','nor','on','at','to','by','in'}\n    words=s.lower().split()\n    return ' '.join(w if i>0 and w in small else w.capitalize() for i,w in enumerate(words))",
        "task": "string",
        "hard": True
    },
    {
        "id": "067",
        "prompt": "Convert a camelCase string to snake_case",
        "code": "import re\ndef reformat_identifier(name):\n    s=re.sub(r'([A-Z]+)([A-Z][a-z])',r'\\1_\\2',name)\n    return re.sub(r'([a-z0-9])([A-Z])',r'\\1_\\2',s).lower()",
        "task": "string",
        "hard": True
    },
    {
        "id": "068",
        "prompt": "Convert a snake_case string to camelCase",
        "code": "def reformat_identifier(name):\n    parts=name.split('_')\n    return parts[0]+''.join(p.capitalize() for p in parts[1:])",
        "task": "string",
        "hard": True
    },
    {
        "id": "069",
        "prompt": "Slugify a string for use in a URL",
        "code": "import re\ndef make_slug(text):\n    s=text.lower().strip()\n    s=re.sub(r'[^\\w\\s-]','',s)\n    return re.sub(r'[\\s_-]+','-',s).strip('-')",
        "task": "string",
        "hard": True
    },
    {
        "id": "070",
        "prompt": "Count the number of words in a string",
        "code": "def count_tokens(text):\n    return len(text.split())",
        "task": "string",
        "hard": True
    },
    {
        "id": "071",
        "prompt": "Wrap text at a given column width without breaking words",
        "code": "import textwrap\ndef reflow(text, width=72):\n    return textwrap.fill(text,width)",
        "task": "string",
        "hard": True
    },
    {
        "id": "072",
        "prompt": "Remove all HTML tags from a string",
        "code": "import re\ndef strip_markup(html):\n    return re.sub(r'<[^>]+>','',html)",
        "task": "string",
        "hard": True
    },
    {
        "id": "073",
        "prompt": "Find all URLs in a block of text",
        "code": "import re\ndef extract_links(text):\n    return re.findall(r'https?://[^\\s<>\"{}|\\\\^`]+',text)",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "074",
        "prompt": "Split a string into sentences",
        "code": "import re\ndef split_sentences(text):\n    return [s.strip() for s in re.split(r'(?<=[.!?])\\s+',text) if s.strip()]",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "075",
        "prompt": "Pad a string on the left to a fixed width with a given character",
        "code": "def align_right(text, width, fill=' '):\n    return text.rjust(width,fill)",
        "task": "string",
        "hard": True
    },
    {
        "id": "076",
        "prompt": "Calculate the percentage change between two values",
        "code": "def compute_delta(old, new):\n    if old==0: raise ValueError('Cannot divide by zero')\n    return ((new-old)/abs(old))*100",
        "task": "math",
        "hard": True
    },
    {
        "id": "077",
        "prompt": "Calculate the mean of a list of numbers",
        "code": "def central_tendency(values):\n    if not values: raise ValueError('Empty list')\n    return sum(values)/len(values)",
        "task": "math",
        "hard": True
    },
    {
        "id": "078",
        "prompt": "Calculate the median of a list of numbers",
        "code": "def midpoint(values):\n    s=sorted(values); n=len(s)\n    if n%2==1: return s[n//2]\n    return (s[n//2-1]+s[n//2])/2",
        "task": "math",
        "hard": True
    },
    {
        "id": "079",
        "prompt": "Calculate the standard deviation of a list of numbers",
        "code": "import math\ndef spread(values):\n    n=len(values)\n    if n<2: raise ValueError('Need at least 2 values')\n    mean=sum(values)/n\n    return math.sqrt(sum((x-mean)**2 for x in values)/(n-1))",
        "task": "math",
        "hard": True
    },
    {
        "id": "080",
        "prompt": "Clamp a number between a minimum and maximum value",
        "code": "def constrain(value, lo, hi):\n    return max(lo,min(hi,value))",
        "task": "math",
        "hard": True
    },
    {
        "id": "081",
        "prompt": "Round a number to a given number of significant figures",
        "code": "import math\ndef round_sig(x, sig):\n    if x==0: return 0\n    d=math.ceil(math.log10(abs(x)))\n    return round(x,sig-d)",
        "task": "math",
        "hard": True
    },
    {
        "id": "082",
        "prompt": "Check if a number is a perfect square",
        "code": "import math\ndef is_exact_square(n):\n    if n<0: return False\n    root=int(math.isqrt(n))\n    return root*root==n",
        "task": "math",
        "hard": True
    },
    {
        "id": "083",
        "prompt": "Find the greatest common divisor of two integers",
        "code": "def shared_factor(a, b):\n    while b: a,b=b,a%b\n    return a",
        "task": "math",
        "hard": True
    },
    {
        "id": "084",
        "prompt": "Generate a list of prime numbers up to n using the Sieve of Eratosthenes",
        "code": "def generate_primes(n):\n    sieve=[True]*(n+1); sieve[0]=sieve[1]=False\n    for i in range(2,int(n**0.5)+1):\n        if sieve[i]:\n            for j in range(i*i,n+1,i): sieve[j]=False\n    return [i for i,v in enumerate(sieve) if v]",
        "task": "math",
        "hard": True
    },
    {
        "id": "085",
        "prompt": "Convert a number from one base to another",
        "code": "def rebase(value, from_base, to_base):\n    decimal=int(str(value),from_base)\n    if to_base==10: return str(decimal)\n    digits=[]\n    while decimal:\n        digits.append('0123456789ABCDEF'[decimal%to_base])\n        decimal//=to_base\n    return ''.join(reversed(digits)) or '0'",
        "task": "math",
        "hard": True
    },
    {
        "id": "086",
        "prompt": "Flatten a nested dictionary to dot-separated keys",
        "code": "def flatten(d, parent='', sep='.'):\n    items={}\n    for k,v in d.items():\n        key=f'{parent}{sep}{k}' if parent else k\n        if isinstance(v,dict): items.update(flatten(v,key,sep))\n        else: items[key]=v\n    return items",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "087",
        "prompt": "Group a list of dictionaries by the value of a given key",
        "code": "def group_by(records, key):\n    groups={}\n    for r in records:\n        v=r.get(key)\n        groups.setdefault(v,[]).append(r)\n    return groups",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "088",
        "prompt": "Paginate a list and return a specific page",
        "code": "def get_page(items, page, size):\n    if page<1 or size<1: raise ValueError('page and size must be positive')\n    start=(page-1)*size\n    return {'items':items[start:start+size],'page':page,'total':len(items),'pages':-(-len(items)//size)}",
        "task": "api",
        "hard": True
    },
    {
        "id": "089",
        "prompt": "Deep copy a nested dictionary without using the copy module",
        "code": "def duplicate(obj):\n    if isinstance(obj,dict): return {k:duplicate(v) for k,v in obj.items()}\n    if isinstance(obj,list): return [duplicate(i) for i in obj]\n    return obj",
        "task": "data",
        "hard": True
    },
    {
        "id": "090",
        "prompt": "Deeply merge two dictionaries with the second overwriting the first on conflicts",
        "code": "def deep_merge(base, override):\n    result=base.copy()\n    for k,v in override.items():\n        if k in result and isinstance(result[k],dict) and isinstance(v,dict):\n            result[k]=deep_merge(result[k],v)\n        else: result[k]=v\n    return result",
        "task": "data",
        "hard": True
    },
    {
        "id": "091",
        "prompt": "Chunk a list into sublists of a fixed size",
        "code": "def partition(items, size):\n    if size<=0: raise ValueError('size must be positive')\n    return [items[i:i+size] for i in range(0,len(items),size)]",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "092",
        "prompt": "Transpose a 2D list (matrix)",
        "code": "def flip_axes(matrix):\n    if not matrix: return []\n    return [list(row) for row in zip(*matrix)]",
        "task": "data",
        "hard": True
    },
    {
        "id": "093",
        "prompt": "Zip multiple lists into a list of tuples stopping at the shortest",
        "code": "def interleave(*sequences):\n    return list(zip(*sequences))",
        "task": "data",
        "hard": True
    },
    {
        "id": "094",
        "prompt": "Find the most common element in a list",
        "code": "def dominant(items):\n    if not items: raise ValueError('empty list')\n    return max(set(items),key=items.count)",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "095",
        "prompt": "Return the unique elements of a list preserving order",
        "code": "def deduplicate(items):\n    seen=set(); result=[]\n    for i in items:\n        if i not in seen: seen.add(i); result.append(i)\n    return result",
        "task": "data",
        "hard": True
    },
    {
        "id": "096",
        "prompt": "Format a datetime object as an ISO 8601 string",
        "code": "from datetime import datetime\ndef to_iso(dt):\n    return dt.strftime('%Y-%m-%dT%H:%M:%S')",
        "task": "datetime",
        "hard": True
    },
    {
        "id": "097",
        "prompt": "Parse an ISO 8601 date string into a datetime object",
        "code": "from datetime import datetime\ndef from_iso(s):\n    return datetime.fromisoformat(s)",
        "task": "datetime",
        "hard": True
    },
    {
        "id": "098",
        "prompt": "Calculate the number of days between two dates",
        "code": "from datetime import date\ndef day_gap(start, end):\n    return abs((end-start).days)",
        "task": "datetime",
        "hard": True
    },
    {
        "id": "099",
        "prompt": "Return the start and end of the week containing a given date",
        "code": "from datetime import date,timedelta\ndef week_bounds(d):\n    start=d-timedelta(days=d.weekday())\n    return start,start+timedelta(days=6)",
        "task": "datetime",
        "hard": True
    },
    {
        "id": "100",
        "prompt": "Convert a Unix timestamp to a datetime object",
        "code": "from datetime import datetime\ndef from_epoch(ts):\n    return datetime.utcfromtimestamp(ts)",
        "task": "datetime",
        "hard": True
    },
    {
        "id": "101",
        "prompt": "Check if a string is a valid UUID",
        "code": "import re\ndef is_valid_id(s):\n    p=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n    return bool(re.match(p,s,re.I))",
        "task": "validation",
        "hard": True
    },
    {
        "id": "102",
        "prompt": "Check if a string is a valid JSON document",
        "code": "import json\ndef is_parseable(s):\n    try: json.loads(s); return True\n    except json.JSONDecodeError: return False",
        "task": "validation",
        "hard": True
    },
    {
        "id": "103",
        "prompt": "Validate that a dictionary contains all required keys",
        "code": "def has_required_fields(data, required):\n    missing=[k for k in required if k not in data]\n    return not missing, missing",
        "task": "validation",
        "hard": True
    },
    {
        "id": "104",
        "prompt": "Check if a value is within an inclusive numeric range",
        "code": "def in_bounds(value, low, high):\n    return low<=value<=high",
        "task": "validation",
        "hard": True
    },
    {
        "id": "105",
        "prompt": "Validate a credit card number using the Luhn algorithm",
        "code": "def passes_luhn(number):\n    digits=[int(d) for d in str(number) if d.isdigit()]\n    digits.reverse()\n    total=sum(digits[i] if i%2==0 else (2*digits[i]-9 if 2*digits[i]>9 else 2*digits[i]) for i in range(len(digits)))\n    return total%10==0",
        "task": "validation",
        "hard": True
    },
    {
        "id": "106",
        "prompt": "Check if a string is a valid hexadecimal colour code",
        "code": "import re\ndef is_valid_colour(s):\n    return bool(re.match(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$',s))",
        "task": "validation",
        "hard": True
    },
    {
        "id": "107",
        "prompt": "Validate a phone number allowing common formats",
        "code": "import re\ndef is_valid_phone(s):\n    return bool(re.match(r'^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$',s))",
        "task": "validation",
        "hard": True
    },
    {
        "id": "108",
        "prompt": "Run multiple functions in parallel and return their results",
        "code": "from concurrent.futures import ThreadPoolExecutor\ndef run_parallel(funcs):\n    with ThreadPoolExecutor() as ex:\n        futures=[ex.submit(f) for f in funcs]\n        return [f.result() for f in futures]",
        "task": "concurrency",
        "hard": True
    },
    {
        "id": "109",
        "prompt": "Run a function with a timeout and raise if it exceeds it",
        "code": "from concurrent.futures import ThreadPoolExecutor,TimeoutError\ndef run_with_timeout(func, timeout, *args, **kwargs):\n    with ThreadPoolExecutor(max_workers=1) as ex:\n        future=ex.submit(func,*args,**kwargs)\n        return future.result(timeout=timeout)",
        "task": "concurrency",
        "hard": True
    },
    {
        "id": "110",
        "prompt": "Implement a simple thread-safe counter",
        "code": "import threading\nclass SharedCounter:\n    def __init__(self): self._val=0; self._lock=threading.Lock()\n    def increment(self):\n        with self._lock: self._val+=1\n    def value(self):\n        with self._lock: return self._val",
        "task": "concurrency",
        "hard": True
    },
    {
        "id": "111",
        "prompt": "Return a JSON response with a status code and message",
        "code": "import json\ndef make_response(status, message, data=None):\n    body={'status':status,'message':message}\n    if data is not None: body['data']=data\n    return json.dumps(body)",
        "task": "api",
        "hard": True
    },
    {
        "id": "112",
        "prompt": "Parse and validate a Bearer token from an Authorization header",
        "code": "def extract_bearer(header):\n    if not header or not header.startswith('Bearer '):\n        raise ValueError('Missing or invalid Authorization header')\n    return header[7:]",
        "task": "api",
        "hard": True
    },
    {
        "id": "113",
        "prompt": "Implement exponential backoff delay for a given attempt number",
        "code": "import time,random\ndef backoff_delay(attempt, base=0.5, cap=30.0, jitter=True):\n    delay=min(base*2**attempt,cap)\n    if jitter: delay*=random.uniform(0.5,1.5)\n    time.sleep(delay)",
        "task": "reliability",
        "hard": True
    },
    {
        "id": "114",
        "prompt": "Build a cursor-based pagination token from an offset",
        "code": "import base64,json\ndef make_cursor(offset, limit):\n    payload=json.dumps({'offset':offset,'limit':limit}).encode()\n    return base64.urlsafe_b64encode(payload).decode()",
        "task": "api",
        "hard": True
    },
    {
        "id": "115",
        "prompt": "Decode a cursor-based pagination token",
        "code": "import base64,json\ndef read_cursor(cursor):\n    payload=base64.urlsafe_b64decode(cursor.encode())\n    return json.loads(payload)",
        "task": "api",
        "hard": True
    },
    {
        "id": "116",
        "prompt": "Format a log message with timestamp, level, and message",
        "code": "from datetime import datetime\ndef format_log(level, message):\n    ts=datetime.now().isoformat()\n    return f'[{ts}] [{level.upper()}] {message}'",
        "task": "observability",
        "hard": True
    },
    {
        "id": "117",
        "prompt": "Count how many times each value appears in a list and return sorted by frequency",
        "code": "def frequency_rank(items):\n    counts={}\n    for i in items: counts[i]=counts.get(i,0)+1\n    return sorted(counts.items(),key=lambda x:-x[1])",
        "task": "data",
        "hard": True
    },
    {
        "id": "118",
        "prompt": "Compute a running total of a list of numbers",
        "code": "def running_total(values):\n    totals=[]; acc=0\n    for v in values: acc+=v; totals.append(acc)\n    return totals",
        "task": "math",
        "hard": True
    },
    {
        "id": "119",
        "prompt": "Diff two dictionaries and return added, removed, and changed keys",
        "code": "def compare_dicts(before, after):\n    added={k:after[k] for k in after if k not in before}\n    removed={k:before[k] for k in before if k not in after}\n    changed={k:(before[k],after[k]) for k in before if k in after and before[k]!=after[k]}\n    return {'added':added,'removed':removed,'changed':changed}",
        "task": "data",
        "hard": True
    },
    {
        "id": "120",
        "prompt": "Convert a list of key-value tuples to a dictionary",
        "code": "def from_pairs(pairs):\n    return dict(pairs)",
        "task": "data",
        "hard": True
    },
    {
        "id": "121",
        "prompt": "Perform a breadth-first search on a graph represented as an adjacency list",
        "code": "from collections import deque\ndef traverse_bfs(graph, start):\n    visited=[]; queue=deque([start]); seen={start}\n    while queue:\n        node=queue.popleft(); visited.append(node)\n        for n in graph.get(node,[]):\n            if n not in seen: seen.add(n); queue.append(n)\n    return visited",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "122",
        "prompt": "Perform a depth-first search on a graph",
        "code": "def traverse_dfs(graph, start, visited=None):\n    if visited is None: visited=[]\n    visited.append(start)\n    for n in graph.get(start,[]):\n        if n not in visited: traverse_dfs(graph,n,visited)\n    return visited",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "123",
        "prompt": "Find the shortest path between two nodes using Dijkstra's algorithm",
        "code": "import heapq\ndef shortest_path(graph, start, end):\n    dist={start:0}; heap=[(0,start)]; prev={}\n    while heap:\n        d,u=heapq.heappop(heap)\n        if u==end: break\n        for v,w in graph.get(u,{}).items():\n            nd=d+w\n            if v not in dist or nd<dist[v]:\n                dist[v]=nd; prev[v]=u; heapq.heappush(heap,(nd,v))\n    path=[]; cur=end\n    while cur in prev: path.append(cur); cur=prev[cur]\n    return [cur]+path[::-1] if cur==start else []",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "124",
        "prompt": "Check if a graph has a cycle",
        "code": "def has_cycle(graph):\n    visited=set(); rec=set()\n    def dfs(node):\n        visited.add(node); rec.add(node)\n        for n in graph.get(node,[]):\n            if n not in visited:\n                if dfs(n): return True\n            elif n in rec: return True\n        rec.discard(node); return False\n    return any(dfs(n) for n in graph if n not in visited)",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "125",
        "prompt": "Topological sort a directed acyclic graph",
        "code": "def topological_order(graph):\n    visited=set(); order=[]\n    def dfs(node):\n        visited.add(node)\n        for n in graph.get(node,[]): \n            if n not in visited: dfs(n)\n        order.append(node)\n    for node in graph:\n        if node not in visited: dfs(node)\n    return order[::-1]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "126",
        "prompt": "Apply a function to every value in a dictionary",
        "code": "def map_values(d, func):\n    return {k:func(v) for k,v in d.items()}",
        "task": "data",
        "hard": True
    },
    {
        "id": "127",
        "prompt": "Filter a dictionary by a predicate on its values",
        "code": "def filter_values(d, predicate):\n    return {k:v for k,v in d.items() if predicate(v)}",
        "task": "data",
        "hard": True
    },
    {
        "id": "128",
        "prompt": "Compose two functions so calling the result applies them in sequence",
        "code": "def compose(f, g):\n    return lambda *a,**k: f(g(*a,**k))",
        "task": "functional",
        "hard": True
    },
    {
        "id": "129",
        "prompt": "Partially apply a function with some arguments pre-filled",
        "code": "import functools\ndef bind(func, *args, **kwargs):\n    return functools.partial(func,*args,**kwargs)",
        "task": "functional",
        "hard": True
    },
    {
        "id": "130",
        "prompt": "Reduce a list to a single value using a binary function",
        "code": "from functools import reduce\ndef fold(items, func, initial=None):\n    return reduce(func,items) if initial is None else reduce(func,items,initial)",
        "task": "functional",
        "hard": True
    },
    {
        "id": "131",
        "prompt": "Strip accents from a unicode string",
        "code": "import unicodedata\ndef strip_accents(s):\n    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')",
        "task": "string",
        "hard": True
    },
    {
        "id": "132",
        "prompt": "Detect the encoding of a byte string",
        "code": "def guess_encoding(data):\n    for enc in ('utf-8','latin-1','utf-16'):\n        try: data.decode(enc); return enc\n        except (UnicodeDecodeError,AttributeError): pass\n    return 'unknown'",
        "task": "string",
        "hard": True
    },
    {
        "id": "133",
        "prompt": "Replace multiple substrings in a string in one pass",
        "code": "import re\ndef replace_many(text, replacements):\n    pattern=re.compile('|'.join(re.escape(k) for k in replacements))\n    return pattern.sub(lambda m:replacements[m.group(0)],text)",
        "task": "string",
        "hard": True
    },
    {
        "id": "134",
        "prompt": "Extract all numbers from a string",
        "code": "import re\ndef pull_numbers(text):\n    return [float(n) if '.' in n else int(n) for n in re.findall(r'-?\\d+\\.?\\d*',text)]",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "135",
        "prompt": "Tokenise a string by splitting on whitespace and punctuation",
        "code": "import re\ndef tokenise(text):\n    return re.findall(r'\\b\\w+\\b',text.lower())",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "136",
        "prompt": "Invert a dictionary swapping keys and values",
        "code": "def invert_map(d):\n    return {v:k for k,v in d.items()}",
        "task": "data",
        "hard": True
    },
    {
        "id": "137",
        "prompt": "Zip two lists into a dictionary",
        "code": "def zip_to_dict(keys, values):\n    return dict(zip(keys,values))",
        "task": "data",
        "hard": True
    },
    {
        "id": "138",
        "prompt": "Flatten a list of lists into a single list",
        "code": "def flatten_once(nested):\n    return [item for sub in nested for item in sub]",
        "task": "data",
        "hard": True
    },
    {
        "id": "139",
        "prompt": "Split a list into two based on a predicate",
        "code": "def bifurcate(items, predicate):\n    yes,no=[],[]\n    for i in items:\n        (yes if predicate(i) else no).append(i)\n    return yes,no",
        "task": "data",
        "hard": True
    },
    {
        "id": "140",
        "prompt": "Sample n random elements from a list without replacement",
        "code": "import random\ndef draw_sample(items, n):\n    return random.sample(items,min(n,len(items)))",
        "task": "data",
        "hard": True
    },
    {
        "id": "141",
        "prompt": "Generate a random UUID",
        "code": "import uuid\ndef new_id():\n    return str(uuid.uuid4())",
        "task": "security",
        "hard": True
    },
    {
        "id": "142",
        "prompt": "Constant-time comparison of two strings to prevent timing attacks",
        "code": "import hmac\ndef safe_compare(a, b):\n    return hmac.compare_digest(a.encode() if isinstance(a,str) else a,\n                               b.encode() if isinstance(b,str) else b)",
        "task": "security",
        "hard": True
    },
    {
        "id": "143",
        "prompt": "Hash a string using SHA-256 and return the hex digest",
        "code": "import hashlib\ndef fingerprint(data):\n    if isinstance(data,str): data=data.encode()\n    return hashlib.sha256(data).hexdigest()",
        "task": "security",
        "hard": True
    },
    {
        "id": "144",
        "prompt": "Generate a random secure password with letters, digits, and symbols",
        "code": "import secrets,string\ndef generate_password(length=16):\n    chars=string.ascii_letters+string.digits+string.punctuation\n    return ''.join(secrets.choice(chars) for _ in range(length))",
        "task": "security",
        "hard": True
    },
    {
        "id": "145",
        "prompt": "XOR encrypt a byte string with a key",
        "code": "def xor_cipher(data, key):\n    return bytes(b^key[i%len(key)] for i,b in enumerate(data))",
        "task": "security",
        "hard": True
    },
    {
        "id": "146",
        "prompt": "Implement a least-recently-used cache with a capacity limit",
        "code": "from collections import OrderedDict\nclass BoundedCache:\n    def __init__(self,cap): self._cap=cap; self._cache=OrderedDict()\n    def get(self,key):\n        if key not in self._cache: return None\n        self._cache.move_to_end(key); return self._cache[key]\n    def put(self,key,val):\n        if key in self._cache: self._cache.move_to_end(key)\n        self._cache[key]=val\n        if len(self._cache)>self._cap: self._cache.popitem(last=False)",
        "task": "data_structure",
        "hard": True
    },
    {
        "id": "147",
        "prompt": "Implement a trie for efficient string prefix search",
        "code": "class PrefixTree:\n    def __init__(self): self.children={}; self.terminal=False\n    def insert(self,word):\n        node=self\n        for ch in word:\n            node=node.children.setdefault(ch,PrefixTree())\n        node.terminal=True\n    def search(self,word):\n        node=self\n        for ch in word:\n            if ch not in node.children: return False\n            node=node.children[ch]\n        return node.terminal",
        "task": "data_structure",
        "hard": True
    },
    {
        "id": "148",
        "prompt": "Implement a min-heap and return elements in sorted order",
        "code": "import heapq\ndef heap_sort(items):\n    h=items[:]; heapq.heapify(h)\n    return [heapq.heappop(h) for _ in range(len(h))]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "149",
        "prompt": "Find the kth largest element in a list",
        "code": "import heapq\ndef kth_largest(items, k):\n    return heapq.nlargest(k,items)[-1]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "150",
        "prompt": "Count the number of islands in a binary grid",
        "code": "def count_regions(grid):\n    if not grid: return 0\n    rows,cols=len(grid),len(grid[0]); count=0\n    def sink(r,c):\n        if r<0 or r>=rows or c<0 or c>=cols or grid[r][c]=='0': return\n        grid[r][c]='0'\n        for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]: sink(r+dr,c+dc)\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c]=='1': count+=1; sink(r,c)\n    return count",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "151",
        "prompt": "Implement the observer pattern with subscribe and notify",
        "code": "class EventBus:\n    def __init__(self): self._handlers={}\n    def subscribe(self,event,handler): self._handlers.setdefault(event,[]).append(handler)\n    def publish(self,event,*args,**kwargs):\n        for h in self._handlers.get(event,[]): h(*args,**kwargs)",
        "task": "design_pattern",
        "hard": True
    },
    {
        "id": "152",
        "prompt": "Implement a simple state machine with transitions",
        "code": "class StateMachine:\n    def __init__(self,initial): self.state=initial; self._transitions={}\n    def add_transition(self,from_state,event,to_state): self._transitions[(from_state,event)]=to_state\n    def trigger(self,event):\n        key=(self.state,event)\n        if key not in self._transitions: raise ValueError(f'No transition for {key}')\n        self.state=self._transitions[key]",
        "task": "design_pattern",
        "hard": True
    },
    {
        "id": "153",
        "prompt": "Implement a pipeline that chains multiple transformation functions",
        "code": "from functools import reduce\ndef make_pipeline(*steps):\n    def run(value): return reduce(lambda v,f:f(v),steps,value)\n    return run",
        "task": "functional",
        "hard": True
    },
    {
        "id": "154",
        "prompt": "Implement a context manager that times a block of code",
        "code": "import time\nclass Timer:\n    def __enter__(self): self.start=time.perf_counter(); return self\n    def __exit__(self,*args): self.elapsed=time.perf_counter()-self.start",
        "task": "performance",
        "hard": True
    },
    {
        "id": "155",
        "prompt": "Implement a context manager that temporarily changes the working directory",
        "code": "import os\nfrom contextlib import contextmanager\n@contextmanager\ndef change_dir(path):\n    old=os.getcwd()\n    try: os.chdir(path); yield\n    finally: os.chdir(old)",
        "task": "io",
        "hard": True
    },
    {
        "id": "156",
        "prompt": "Parse a query string into a dictionary",
        "code": "from urllib.parse import parse_qs,unquote_plus\ndef parse_query(qs):\n    return {k:v[0] if len(v)==1 else v for k,v in parse_qs(qs).items()}",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "157",
        "prompt": "Parse a simple key=value config file into a dictionary",
        "code": "def parse_config(text):\n    result={}\n    for line in text.splitlines():\n        line=line.strip()\n        if not line or line.startswith('#'): continue\n        k,_,v=line.partition('=')\n        result[k.strip()]=v.strip()\n    return result",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "158",
        "prompt": "Extract all key-value pairs from an HTML attributes string",
        "code": "import re\ndef parse_attributes(s):\n    return {m.group(1):m.group(2) or m.group(3) or m.group(4)\n            for m in re.finditer(r'(\\w+)(?:=[\"\\']([^\"\\']*)[\"\\']|=(\\S+)|(\\w+))',s)}",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "159",
        "prompt": "Convert a nested list to a tree-formatted string",
        "code": "def tree_format(node, prefix='', is_last=True):\n    connector='`-- ' if is_last else '|-- '\n    lines=[prefix+connector+str(node[0])]\n    children=node[1:]\n    for i,child in enumerate(children):\n        ext=' ' if is_last else '|   '\n        lines.extend(tree_format(child,prefix+ext,i==len(children)-1))\n    return lines",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "160",
        "prompt": "Extract structured data from a log line with a known format",
        "code": "import re\ndef parse_log_line(line):\n    m=re.match(r'\\[(.+?)\\] \\[(.+?)\\] (.+)',line)\n    if not m: return None\n    return {'timestamp':m.group(1),'level':m.group(2),'message':m.group(3)}",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "161",
        "prompt": "Compute all prime factors of a number",
        "code": "def prime_factors(n):\n    factors=[]\n    d=2\n    while d*d<=n:\n        while n%d==0: factors.append(d); n//=d\n        d+=1\n    if n>1: factors.append(n)\n    return factors",
        "task": "math",
        "hard": True
    },
    {
        "id": "162",
        "prompt": "Check whether two rectangles overlap",
        "code": "def rectangles_overlap(r1, r2):\n    return not (r1[2]<=r2[0] or r2[2]<=r1[0] or r1[3]<=r2[1] or r2[3]<=r1[1])",
        "task": "math",
        "hard": True
    },
    {
        "id": "163",
        "prompt": "Calculate the Euclidean distance between two points in 2D",
        "code": "import math\ndef point_distance(p1, p2):\n    return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)",
        "task": "math",
        "hard": True
    },
    {
        "id": "164",
        "prompt": "Interpolate a value linearly between two points",
        "code": "def lerp(a, b, t):\n    return a+(b-a)*t",
        "task": "math",
        "hard": True
    },
    {
        "id": "165",
        "prompt": "Normalise a list of numbers to the range 0 to 1",
        "code": "def normalise(values):\n    lo,hi=min(values),max(values)\n    if lo==hi: return [0.0]*len(values)\n    return [(v-lo)/(hi-lo) for v in values]",
        "task": "math",
        "hard": True
    },
    {
        "id": "166",
        "prompt": "Compute a moving average over a list of numbers with a given window",
        "code": "def moving_average(values, window):\n    return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]",
        "task": "math",
        "hard": True
    },
    {
        "id": "167",
        "prompt": "Pivot a list of records into a dictionary keyed by a field",
        "code": "def pivot_on(records, key):\n    return {r[key]:r for r in records}",
        "task": "data",
        "hard": True
    },
    {
        "id": "168",
        "prompt": "Compute the Cartesian product of multiple lists",
        "code": "from itertools import product\ndef all_combinations(*iterables):\n    return list(product(*iterables))",
        "task": "data",
        "hard": True
    },
    {
        "id": "169",
        "prompt": "Accumulate values in a dictionary by adding to existing entries",
        "code": "def accumulate(d, key, value):\n    d[key]=d.get(key,0)+value\n    return d",
        "task": "data",
        "hard": True
    },
    {
        "id": "170",
        "prompt": "Convert a flat list of parent-child pairs into a tree structure",
        "code": "def build_tree(pairs):\n    nodes={}\n    for parent,child in pairs:\n        nodes.setdefault(parent,{}).setdefault('children',[])\n        nodes.setdefault(child,{}).setdefault('children',[])\n        nodes[parent]['children'].append(nodes[child])\n    roots={p for p,_ in pairs}-{c for _,c in pairs}\n    return [nodes[r] for r in roots]",
        "task": "data",
        "hard": True
    },
    {
        "id": "171",
        "prompt": "Implement a circuit breaker that stops calling a failing function after a threshold",
        "code": "class CircuitBreaker:\n    def __init__(self,threshold=3): self._fails=0; self._threshold=threshold; self._open=False\n    def call(self,func,*args,**kwargs):\n        if self._open: raise RuntimeError('Circuit open')\n        try:\n            result=func(*args,**kwargs); self._fails=0; return result\n        except Exception:\n            self._fails+=1\n            if self._fails>=self._threshold: self._open=True\n            raise",
        "task": "reliability",
        "hard": True
    },
    {
        "id": "172",
        "prompt": "Implement a token bucket for rate limiting",
        "code": "import time\nclass TokenBucket:\n    def __init__(self,rate,capacity):\n        self._rate=rate; self._cap=capacity; self._tokens=capacity; self._last=time.time()\n    def consume(self,tokens=1):\n        now=time.time(); self._tokens=min(self._cap,self._tokens+(now-self._last)*self._rate)\n        self._last=now\n        if self._tokens<tokens: return False\n        self._tokens-=tokens; return True",
        "task": "reliability",
        "hard": True
    },
    {
        "id": "173",
        "prompt": "Implement a simple in-memory key-value store with TTL expiry",
        "code": "import time\nclass EphemeralStore:\n    def __init__(self): self._data={}\n    def set(self,key,value,ttl=None):\n        self._data[key]=(value,time.time()+ttl if ttl else None)\n    def get(self,key):\n        if key not in self._data: return None\n        value,exp=self._data[key]\n        if exp and time.time()>exp: del self._data[key]; return None\n        return value",
        "task": "data_structure",
        "hard": True
    },
    {
        "id": "174",
        "prompt": "Batch items from a generator into fixed-size chunks",
        "code": "from itertools import islice\ndef batch(iterable, size):\n    it=iter(iterable)\n    while True:\n        chunk=list(islice(it,size))\n        if not chunk: break\n        yield chunk",
        "task": "data",
        "hard": True
    },
    {
        "id": "175",
        "prompt": "Retry an operation until it succeeds or a deadline passes",
        "code": "import time\ndef retry_until(func, deadline, interval=0.5):\n    end=time.time()+deadline\n    while time.time()<end:\n        try: return func()\n        except Exception:\n            if time.time()+interval>=end: raise\n            time.sleep(interval)\n    raise TimeoutError('Deadline exceeded')",
        "task": "reliability",
        "hard": True
    },
    {
        "id": "176",
        "prompt": "Atomically write a file by writing to a temp file and renaming",
        "code": "import os,tempfile\ndef atomic_write(path, content):\n    dir=os.path.dirname(os.path.abspath(path))\n    fd,tmp=tempfile.mkstemp(dir=dir)\n    try:\n        with os.fdopen(fd,'w') as f: f.write(content)\n        os.replace(tmp,path)\n    except:\n        os.unlink(tmp); raise",
        "task": "io",
        "hard": True
    },
    {
        "id": "177",
        "prompt": "Lock a file to prevent concurrent writes",
        "code": "import fcntl\nfrom contextlib import contextmanager\n@contextmanager\ndef file_lock(path):\n    with open(path,'a') as f:\n        fcntl.flock(f,fcntl.LOCK_EX)\n        try: yield f\n        finally: fcntl.flock(f,fcntl.LOCK_UN)",
        "task": "io",
        "hard": True
    },
    {
        "id": "178",
        "prompt": "Tail a file and yield new lines as they are appended",
        "code": "import time\ndef follow(path, poll=0.1):\n    with open(path) as f:\n        f.seek(0,2)\n        while True:\n            line=f.readline()\n            if not line: time.sleep(poll); continue\n            yield line.rstrip()",
        "task": "io",
        "hard": True
    },
    {
        "id": "179",
        "prompt": "Recursively delete a directory and all its contents",
        "code": "import shutil,os\ndef remove_tree(path):\n    if os.path.isdir(path): shutil.rmtree(path)\n    elif os.path.exists(path): os.remove(path)",
        "task": "io",
        "hard": True
    },
    {
        "id": "180",
        "prompt": "Get the size of a directory in bytes recursively",
        "code": "import os\ndef dir_size(path):\n    total=0\n    for dirpath,_,files in os.walk(path):\n        for f in files:\n            try: total+=os.path.getsize(os.path.join(dirpath,f))\n            except OSError: pass\n    return total",
        "task": "io",
        "hard": True
    },
    {
        "id": "181",
        "prompt": "Check if a string is a valid Python identifier",
        "code": "def is_identifier(s):\n    return s.isidentifier() and not __import__('keyword').iskeyword(s)",
        "task": "validation",
        "hard": True
    },
    {
        "id": "182",
        "prompt": "Validate that a list is sorted in ascending order",
        "code": "def is_sorted(items):\n    return all(items[i]<=items[i+1] for i in range(len(items)-1))",
        "task": "validation",
        "hard": True
    },
    {
        "id": "183",
        "prompt": "Check if a string contains only ASCII characters",
        "code": "def is_ascii(s):\n    try: s.encode('ascii'); return True\n    except UnicodeEncodeError: return False",
        "task": "validation",
        "hard": True
    },
    {
        "id": "184",
        "prompt": "Check if a number is a power of two",
        "code": "def is_power_of_two(n):\n    return n>0 and (n&(n-1))==0",
        "task": "validation",
        "hard": True
    },
    {
        "id": "185",
        "prompt": "Validate an ISO 8601 date string",
        "code": "from datetime import datetime\ndef is_valid_date(s):\n    try: datetime.fromisoformat(s); return True\n    except ValueError: return False",
        "task": "validation",
        "hard": True
    },
    {
        "id": "186",
        "prompt": "Find the maximum subarray sum using Kadane's algorithm",
        "code": "def max_subarray(nums):\n    best=cur=nums[0]\n    for n in nums[1:]:\n        cur=max(n,cur+n); best=max(best,cur)\n    return best",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "187",
        "prompt": "Check if a string of brackets is balanced",
        "code": "def is_balanced(s):\n    stack=[]; pairs={')':'(',']':'[','}':'{'}\n    for ch in s:\n        if ch in '([{': stack.append(ch)\n        elif ch in pairs:\n            if not stack or stack[-1]!=pairs[ch]: return False\n            stack.pop()\n    return not stack",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "188",
        "prompt": "Find all unique paths through a grid from top-left to bottom-right",
        "code": "def count_paths(m, n):\n    dp=[[1]*n for _ in range(m)]\n    for i in range(1,m):\n        for j in range(1,n): dp[i][j]=dp[i-1][j]+dp[i][j-1]\n    return dp[m-1][n-1]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "189",
        "prompt": "Evaluate a mathematical expression given as a string",
        "code": "def evaluate(expr):\n    return eval(compile(expr,'<string>','eval'),{'__builtins__':{}},{'abs':abs,'round':round})",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "190",
        "prompt": "Find the edit distance between two strings",
        "code": "def edit_distance(s1, s2):\n    m,n=len(s1),len(s2)\n    dp=[[0]*(n+1) for _ in range(m+1)]\n    for i in range(m+1): dp[i][0]=i\n    for j in range(n+1): dp[0][j]=j\n    for i in range(1,m+1):\n        for j in range(1,n+1):\n            if s1[i-1]==s2[j-1]: dp[i][j]=dp[i-1][j-1]\n            else: dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])\n    return dp[m][n]",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "191",
        "prompt": "Compute a weighted average given values and their weights",
        "code": "def weighted_mean(values, weights):\n    return sum(v*w for v,w in zip(values,weights))/sum(weights)",
        "task": "math",
        "hard": True
    },
    {
        "id": "192",
        "prompt": "Convert a duration in seconds to a human-readable string",
        "code": "def humanise_duration(seconds):\n    parts=[]\n    for unit,size in [('d',86400),('h',3600),('m',60),('s',1)]:\n        if seconds>=size: parts.append(f'{int(seconds//size)}{unit}'); seconds%=size\n    return ' '.join(parts) or '0s'",
        "task": "string",
        "hard": True
    },
    {
        "id": "193",
        "prompt": "Implement a publish-subscribe event system",
        "code": "class Dispatcher:\n    def __init__(self): self._subs={}\n    def on(self,event,fn): self._subs.setdefault(event,[]).append(fn)\n    def emit(self,event,*a,**k):\n        for fn in self._subs.get(event,[]): fn(*a,**k)",
        "task": "design_pattern",
        "hard": True
    },
    {
        "id": "194",
        "prompt": "Convert a list of objects to a CSV string using given field names",
        "code": "import csv,io\ndef to_csv(records, fields):\n    buf=io.StringIO()\n    w=csv.DictWriter(buf,fieldnames=fields,extrasaction='ignore')\n    w.writeheader(); w.writerows(records)\n    return buf.getvalue()",
        "task": "io",
        "hard": True
    },
    {
        "id": "195",
        "prompt": "Find the first element in a list satisfying a predicate",
        "code": "def find_first(items, predicate):\n    return next((i for i in items if predicate(i)),None)",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "196",
        "prompt": "Return a dictionary with keys and values swapped, handling duplicate values",
        "code": "def invert_multimap(d):\n    result={}\n    for k,v in d.items(): result.setdefault(v,[]).append(k)\n    return result",
        "task": "data",
        "hard": True
    },
    {
        "id": "197",
        "prompt": "Detect if a list is a rotation of another list",
        "code": "def is_rotation(a, b):\n    if len(a)!=len(b): return False\n    doubled=a+a\n    return any(doubled[i:i+len(b)]==b for i in range(len(a)))",
        "task": "algorithm",
        "hard": True
    },
    {
        "id": "198",
        "prompt": "Walk a JSON-like nested structure and yield every leaf value with its path",
        "code": "def walk_leaves(obj, path=()):\n    if isinstance(obj,dict):\n        for k,v in obj.items(): yield from walk_leaves(v,path+(k,))\n    elif isinstance(obj,list):\n        for i,v in enumerate(obj): yield from walk_leaves(v,path+(i,))\n    else: yield path,obj",
        "task": "parsing",
        "hard": True
    },
    {
        "id": "199",
        "prompt": "Run a list of tasks concurrently and collect results preserving order",
        "code": "from concurrent.futures import ThreadPoolExecutor\ndef gather(tasks):\n    with ThreadPoolExecutor() as ex:\n        futures=[ex.submit(t) for t in tasks]\n        return [f.result() for f in futures]",
        "task": "concurrency",
        "hard": True
    },
    {
        "id": "200",
        "prompt": "Compute a fingerprint of a Python object by hashing its JSON representation",
        "code": "import hashlib,json\ndef object_hash(obj):\n    serialised=json.dumps(obj,sort_keys=True,default=str).encode()\n    return hashlib.sha256(serialised).hexdigest()",
        "task": "security",
        "hard": True
    }
]

def main():
    output_path = "data/dataset.json"
    with open(output_path, "w") as f:
        json.dump(PAIRS, f, indent=2)

if __name__ == "__main__":
    main()