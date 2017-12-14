# LocalBitcoins API


Documentation: https://localbitcoins.com/api-docs/

To generate `hmac_auth_key`, `hmac_secret_key` go to: https://localbitcoins.com/accounts/api/


## Usage

```python
import localbitcoins
api = localbitcoins.API(hmac_auth_key, hmac_secret_key, debug=False)
api.ads()
```
