from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

class Threader:
    
    @staticmethod
    def thread_iterable(entities, func, max_workers=100) -> list:

        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(func, e): e for e in entities}

            for f in tqdm(as_completed(futures), total=len(futures), desc="Threading task..."):
                data = f.result()
                if data:
                    results.append(data)

        return results