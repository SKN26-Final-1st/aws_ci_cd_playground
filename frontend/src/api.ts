export async function getPing() {
    const response = await fetch(
        "http://127.0.0.1:8000/api/ping/"
    )

    return await response.json()
}