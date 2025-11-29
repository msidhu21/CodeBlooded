from typing import List
from ..repos.csv_repo import CSVRepository

def recommend_items_for_query(query: str, limit: int = 10) -> tuple[List[dict], int]:
    if not query or not query.strip():
        return [], 0
    
    repo = CSVRepository()
    query_lower = query.strip().lower()
    query_tokens = set(query_lower.split())
    
    all_products = repo.df.to_dict('records')
    scored_items = []
    
    for product in all_products:
        score = 0.0
        
        product_name = str(product.get('product_name', '')).lower()
        category = str(product.get('category', '')).lower()
        description = str(product.get('about_product', '')).lower()
        
        if query_lower in product_name:
            score += 3.0
        
        if query_lower in category:
            score += 2.0
        
        if query_lower in description:
            score += 1.0
        
        name_tokens = set(product_name.split())
        category_tokens = set(category.split())
        desc_tokens = set(description.split())
        
        all_item_tokens = name_tokens | category_tokens | desc_tokens
        
        matching_tokens = query_tokens & all_item_tokens
        token_bonus = len(matching_tokens) * 0.5
        score += token_bonus
        
        if score > 0:
            product_with_score = product.copy()
            product_with_score['score'] = round(score, 2)
            scored_items.append(product_with_score)
    
    scored_items.sort(key=lambda x: x['score'], reverse=True)
    
    total_found = len(scored_items)
    limited_items = scored_items[:limit]
    
    return limited_items, total_found

