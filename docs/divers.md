# Divers

The resource linked to sample collectors, AKA divers.

## Available methods

<details>
<summary><code>GET /api/v1/divers</code></summary>

`RESULT`

```
[
    {
        "id": 1,
        "first_name": "Jane",
        "last_name": "Diver-one",
        "institution": "SFU",
        "notes": "Sample diver 1",
        "samples":
            {
                "links": [
                    "BASE_URL/api/v1/samples/1",
                    "BASE_URL/api/v1/samples/2",
                ]
            }
    },
    {
        "id": 2,
        "first_name": "Jack",
        "last_name": "Diver-two",
        "institution": "SFU",
        "notes": "Sample diver 2",
        "samples":
            {
                "links": [
                    "BASE_URL/api/v1/samples/1",
                    "BASE_URL/api/v1/samples/2",
                ]
            }
    }
]
```
</details>

<details>
<summary><code>GET /api/v1/divers/:id</code></summary>

`RESULT`

```
{
    "id": 1,
    "first_name": "Jane",
    "last_name": "Diver-one",
    "institution": "SFU",
    "notes": "Sample diver 1",
    "samples":
        {
            "links": [
                "BASE_URL/api/v1/samples/1",
                "BASE_URL/api/v1/samples/2",
            ]
        }
}
```
</details>