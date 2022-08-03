from concurrent.futures import ThreadPoolExecutor

new_loop = None
_executor = ThreadPoolExecutor(4)