import pandas as pd
import os

# Test 1: Veri dosyasının varlığını kontrol et
def test_file_exists():
    assert os.path.exists("cowrie_data.json") == True

# Test 2: JSON dosyasının Pandas tarafından okunabildiğini kontrol et
def test_pandas_read():
    df = pd.read_json("cowrie_data.json", lines=True)
    assert isinstance(df, pd.DataFrame)

# Test 3: Gerekli sütunların (ip, timestamp) varlığını kontrol et
def test_columns_check():
    df = pd.read_json("cowrie_data.json", lines=True)
    assert 'src_ip' in df.columns
    assert 'timestamp' in df.columns

# Test 4: Logların boş olmadığını kontrol et
def test_data_not_empty():
    df = pd.read_json("cowrie_data.json", lines=True)
    assert len(df) > 0

# Test 5: IP adreslerinin formatının doğruluğunu kontrolü 
def test_ip_format():
    df = pd.read_json("cowrie_data.json", lines=True)
    sample_ip = df['src_ip'].iloc[0]
    assert "." in sample_ip 