import logging
import pandas as pd
from typing import List
from pathlib import Path
from .models import Proxy, ProxyStatus

class ProxyStorage:
    def __init__(self, csv_path: Path):
        self.path = csv_path
        self.columns = ["protocol", "host", "port", "status"]

    def save_proxies(self, proxies: List[Proxy]):
        logging.info(f"Writing {len(proxies)} results to {self.path}...")
        try:
            if self.path.exists():
                df = pd.read_csv(self.path)
            else:
                df = pd.DataFrame(columns=self.columns)
            
            df.set_index(["protocol", "host", "port"], inplace=True) # Use a multi-index for efficient updates
            for p in proxies:
                df.loc[(p.protocol, p.host, p.port), "status"] = p.status.value

            df.reset_index().to_csv(self.path, index=False)
            logging.info("CSV file successfully written.")

        except Exception as e:
            logging.error(f"Failed to write to CSV file: {e}")

    def load_from_text(self, txt_path: Path) -> List[Proxy]:
        if not txt_path.exists():
            raise FileNotFoundError(f"Text file not found: {txt_path}")
            
        proxies: List[Proxy] = []
        lines = txt_path.read_text().splitlines()
        
        for line in lines:
            if "://" not in line:
                logging.warning(f"Skipping malformed line: {line}")
                continue
            
            protocol, address = line.strip().split("://", 1)
            if ":" not in address:
                logging.warning(f"Skipping line with no port: {line}")
                continue
            
            host, port_str = address.split(":", 1)
            proxies.append(Proxy(protocol, host, int(port_str)))
            
        return proxies
        
    def load_from_csv(self) -> List[Proxy]:
        if not self.path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.path}")

        df = pd.read_csv(self.path)
        return [
            Proxy(
                row['protocol'], 
                row['host'], 
                int(row['port']), 
                ProxyStatus(row['status'])
            ) 
            for _, row in df.iterrows()
        ]