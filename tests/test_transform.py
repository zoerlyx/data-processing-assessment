
import pandas as pd
from utils.transform import transform_data

# Definisikan sample data dulu!
df_transform_sample = pd.DataFrame({
    "title": ["T-shirt 2", "Hoodie 3", "Pants 4"],
    "price": ["$16,344.00", "$79,500.80", "$74,769.60"],
    "rating": ["Rating: 3.9 / 5", "Rating: 4.8 / 5", "Rating: 3.3 / 5"],
    "colors": ["3 Colors", "3 Colors", "3 Colors"],
    "size": ["Size: M", "Size: L", "Size: XL"],
    "gender": ["Gender: Women", "Gender: Unisex", "Gender: Men"],
    "timestamp": [None, None, None]
})

# Jalankan test transform
df_test_transform = transform_data(df_transform_sample)

assert df_test_transform.isnull().sum().sum() == 0
assert str(df_test_transform["price"].dtype) in ["int64", "float64"]
assert str(df_test_transform["rating"].dtype).startswith("float")
assert df_test_transform["colors"].dtype == "int64"   # ← pastikan int64!
assert "timestamp" in df_test_transform.columns
assert df_test_transform["timestamp"].notnull().all()


