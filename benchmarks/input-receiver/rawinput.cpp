#include "../common/Common.h"
#include <iostream>
using namespace bench;
namespace {fs::path out;json cfg;std::vector<std::array<int64_t,4>> rows;uint64_t began=0,last=0;volatile LONG* rawAck=nullptr;HANDLE rawEvent=nullptr;
LRESULT CALLBACK window(HWND h,UINT msg,WPARAM w,LPARAM l){
 if(msg==WM_INPUT){
  UINT size=0;GetRawInputData(reinterpret_cast<HRAWINPUT>(l),RID_INPUT,nullptr,&size,sizeof(RAWINPUTHEADER));if(size>=sizeof(RAWINPUTHEADER)&&size<65536){std::vector<uint8_t> b(size);if(GetRawInputData(reinterpret_cast<HRAWINPUT>(l),RID_INPUT,b.data(),&size,sizeof(RAWINPUTHEADER))!=UINT(-1)){
   auto received=qpc();auto* raw=reinterpret_cast<RAWINPUT*>(b.data());wchar_t name[2048]{};UINT n=2048;GetRawInputDeviceInfoW(raw->header.hDevice,RIDI_DEVICENAME,name,&n);std::wstring path=name;std::transform(path.begin(),path.end(),path.begin(),::towupper);
   const bool mouse=cfg.at("profile")=="mouse";
   if(path.find(mouse?L"VID_FFFF&PID_B752":L"VID_FFFF&PID_B753")!=std::wstring::npos){
    int64_t sequence=0;bool valid=false;
    if(mouse&&raw->header.dwType==RIM_TYPEMOUSE){auto x=raw->data.mouse.lLastX,y=raw->data.mouse.lLastY;sequence=std::abs(x)-1;valid=(cfg.value("operation",std::string("forward"))=="modify"?x<0:x>0)&&y==-std::abs(x);}
    else if(!mouse&&raw->header.dwType==RIM_TYPEKEYBOARD){sequence=int64_t(rows.size());auto& k=raw->data.keyboard;valid=k.MakeCode==((sequence/2)%2?0x30:0x1e)&&bool(k.Flags&RI_KEY_BREAK)==bool(sequence%2);}
    rows.push_back({sequence,0,received,valid?1:0});last=GetTickCount64();
    if(mouse&&rawAck&&valid){InterlockedExchange(rawAck,LONG(sequence+1));SetEvent(rawEvent);}
   }
  }}
 }
 if(msg==WM_TIMER){if(GetTickCount64()-began>650000||(fs::exists(out/"generator-done.json")&&GetTickCount64()-last>2000))DestroyWindow(h);}
 if(msg==WM_DESTROY){PostQuitMessage(0);return 0;}return DefWindowProcW(h,msg,w,l);
}}
int wmain(int argc,wchar_t** argv){try{if(argc!=2)return 2;guard();out=argv[1];require(waitfile(out/"run.json",30000),"Run configuration");cfg=load(out/"run.json");require(cfg.at("profile")=="mouse"||cfg.at("profile")=="keyboard","Raw input profile");
 Handle mapping,event;struct Unmap {~Unmap(){if(rawAck)UnmapViewOfFile(const_cast<LONG*>(rawAck));}}unmap;
 if(cfg.contains("raw_channel")){auto name=fs::u8path(cfg.at("raw_channel").get<std::string>()).wstring();mapping.value=OpenFileMappingW(FILE_MAP_ALL_ACCESS,FALSE,name.c_str());require(mapping.value!=nullptr,"Open raw channel");rawAck=static_cast<LONG*>(MapViewOfFile(mapping.value,FILE_MAP_ALL_ACCESS,0,0,sizeof(LONG)));require(rawAck!=nullptr,"Map raw channel");event.value=OpenEventW(EVENT_MODIFY_STATE,FALSE,(name+L"-ack").c_str());require(event.value!=nullptr,"Open raw ack event");rawEvent=event.value;}
 WNDCLASSW cls{};cls.hInstance=GetModuleHandleW(nullptr);cls.lpfnWndProc=window;cls.lpszClassName=L"TitanCSAIndependentRawInput";require(RegisterClassW(&cls)!=0,"Register raw window");HWND h=CreateWindowW(cls.lpszClassName,L"Benchmark receiver",0,0,0,0,0,HWND_MESSAGE,nullptr,cls.hInstance,nullptr);require(h!=nullptr,"Create raw window");RAWINPUTDEVICE d{1,USHORT(cfg.at("profile")=="mouse"?2:6),RIDEV_INPUTSINK,h};require(RegisterRawInputDevices(&d,1,sizeof(d))!=FALSE,"Register raw input");began=last=GetTickCount64();SetTimer(h,1,100,nullptr);save(out/"receiver-ready.json",{{"api","Windows Raw Input"},{"qpc_frequency",frequency()}});MSG m{};while(GetMessageW(&m,nullptr,0,0)>0){TranslateMessage(&m);DispatchMessageW(&m);}std::ofstream f(out/"reception.csv");f<<"sequence,submit_qpc,receive_qpc,content_valid\n";for(auto r:rows)f<<r[0]<<','<<r[1]<<','<<r[2]<<','<<r[3]<<'\n';f.close();save(out/"receiver-done.json",{{"received",rows.size()},{"resources",resources()}});return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';if(!out.empty()&&fs::exists(out))save(out/"receiver-error.json",{{"error",e.what()}});return 1;}}
