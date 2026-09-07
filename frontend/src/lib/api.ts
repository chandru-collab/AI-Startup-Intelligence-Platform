const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';


export const startResearch = async (startupName: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/startups/research`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ startup_name: startupName })
        });
        if (!response.ok) throw new Error("Failed to start research");
        return await response.json();
    } catch (e) {
        console.error(e);
        return { status: "error" };
    }
};
