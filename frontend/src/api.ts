export async function getPing() {
    const response = await fetch("/api/ping/")
    return await response.json()
}