import re

class DataProcessor:
    @staticmethod
    def to_num(txt):
        try:
            num_str = "".join(re.findall(r'\d+', txt.split(',')[0].replace('.', '')))
            return int(num_str) if num_str else 9999999
        except: return 9999999

    def prepare_final_list(self, raw_data_list):
        final_list = []
        seen_names = set()

        for item in raw_data_list:
            name_lower = item['name'].strip().lower()
            numeric_price = self.to_num(item['price_display'])
            
            if name_lower not in seen_names:
                final_list.append((
                    item['store'], 
                    item['name'], 
                    item['price_display'], 
                    numeric_price
                ))
                seen_names.add(name_lower)
        
        # Sort by cheapest
        final_list.sort(key=lambda x: x[3])
        return final_list