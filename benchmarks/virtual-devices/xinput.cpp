#include "../common/XInputChannel.h"
#include <ViGEm/Client.h>
#define VDEVICE_EXAMPLE_TEST
#include "Xbox360.cpp"
#include "XboxOneGip.cpp"
#include "DualShock4.cpp"
#include "ExampleRuntime.h"
#include <iostream>
using namespace bench;
int wmain(int argc,wchar_t** argv){try{
 if(argc!=4)return 2;guard();auto cfg=load(argv[1]);fs::path out=argv[2];std::wstring receiver=argv[3];require(!fs::exists(out),"Existing output");fs::create_directories(out);
 auto backend=cfg.at("backend").get<std::string>();require(backend=="vdevice"||backend=="vigem","Unknown backend");auto count=cfg.at("samples").get<unsigned>(),warm=cfg.at("warmup").get<unsigned>();require(count>0&&count+warm<30000,"Bounded sequence");
 auto profile=cfg.value("profile",std::string("xbox360"));require(profile=="xbox360"||profile=="ds4"||profile=="xbox-one-gip","Controller profile");require(backend!="vigem"||profile!="xbox-one-gip","ViGEm does not implement this GIP profile");std::unique_ptr<Examples::Protocol> model;if(profile=="ds4")model=std::make_unique<DualShock4Example::DualShock4>();else if(profile=="xbox-one-gip")model=std::make_unique<XboxOneGipExample::XboxOneGip>();else model=std::make_unique<Xbox360Example::Xbox360>();
 PVIGEM_CLIENT client=nullptr;PVIGEM_TARGET target=nullptr;Examples::Session session(*model,[](const std::string&){});
 struct Cleanup {Examples::Session& session;PVIGEM_CLIENT& client;PVIGEM_TARGET& target;~Cleanup(){session.Close();if(target){vigem_target_remove(client,target);vigem_target_free(target);}if(client){vigem_disconnect(client);vigem_free(client);}}} cleanup{session,client,target};
 auto created=qpc();if(backend=="vdevice"){session.Open();auto end=GetTickCount64()+30000;while(!session.IsReady()&&GetTickCount64()<end)Sleep(10);require(session.IsReady(),"Vdevice X360 ready");}
 else {client=vigem_alloc();require(client!=nullptr,"ViGEm allocate");require(VIGEM_SUCCESS(vigem_connect(client)),"ViGEm connect");target=profile=="ds4"?vigem_target_ds4_alloc():vigem_target_x360_alloc();require(target!=nullptr,"ViGEm target");require(VIGEM_SUCCESS(vigem_target_add(client,target)),"ViGEm add");}
 cfg["fixture_revision"]="stable-usb-instance-v1";cfg["creation_to_sdk_ready_ticks"]=qpc()-created;cfg["qpc_frequency"]=frequency();cfg["measurement"]="SDK state update entry to separate process XInput state visibility; closed loop";save(out/"xinput-run.json",cfg);
 if(profile=="ds4"){cfg["measurement"]="SDK DS4 update entry to independent Windows HID ReadFile completion; closed loop";save(out/"xinput-run.json",cfg);}
 if(cfg.value("collect_stack",false))require(waitfile(out/"stack-captured.json",60000),"PnP capture deadline");
 auto name=L"Local\\TitanCSABenchmark-"+std::to_wstring(GetCurrentProcessId())+L"-"+std::to_wstring(GetTickCount64());
 Handle mapping(CreateFileMappingW(INVALID_HANDLE_VALUE,nullptr,PAGE_READWRITE,0,sizeof(XInputChannel),name.c_str()));require(mapping.value!=nullptr,"Create channel");auto* channel=static_cast<XInputChannel*>(MapViewOfFile(mapping.value,FILE_MAP_ALL_ACCESS,0,0,sizeof(XInputChannel)));require(channel!=nullptr,"Map channel");ZeroMemory(channel,sizeof(*channel));Handle ack(CreateEventW(nullptr,FALSE,FALSE,(name+L"-ack").c_str()));require(ack.value!=nullptr,"Ack event");
 std::wstring cmd=L"\""+receiver+L"\" \""+out.wstring()+L"\" \""+name+L"\"";STARTUPINFOW si{};si.cb=sizeof(si);PROCESS_INFORMATION pi{};require(CreateProcessW(receiver.c_str(),cmd.data(),nullptr,nullptr,FALSE,CREATE_NO_WINDOW,nullptr,nullptr,&si,&pi)!=FALSE,"Launch independent XInput receiver");Handle process(pi.hProcess),thread(pi.hThread);
 struct Stop {XInputChannel* p;HANDLE process;~Stop(){InterlockedExchange(&p->stop,1);if(WaitForSingleObject(process,10000)!=WAIT_OBJECT_0)TerminateProcess(process,1);UnmapViewOfFile(p);}}stop{channel,process.value};
 auto end=GetTickCount64()+30000;while(!InterlockedCompareExchange(&channel->ready,0,0)&&GetTickCount64()<end)Sleep(10);require(channel->ready!=0,"Receiver XInput enumeration deadline");std::vector<std::array<int64_t,3>> rows;rows.reserve(count+warm);
 for(unsigned n=1;n<=count+warm;++n){ResetEvent(ack.value);auto start=qpc();channel->sent=start;InterlockedExchange(&channel->expected,LONG(n));
  if(profile=="ds4"){
   if(backend=="vdevice")session.Apply({{"buttons",int(1u<<(n%12))},{"hat",int(n%8)},{"lx",int(n&255)},{"ly",255-int(n&255)},{"rx",int((3*n)&255)},{"ry",255-int((3*n)&255)},{"lt",int(n&255)},{"rt",255-int(n&255)}});
   else {DS4_REPORT r{};r.bThumbLX=BYTE(n);r.bThumbLY=BYTE(255-(n&255));r.bThumbRX=BYTE(3*n);r.bThumbRY=BYTE(255-((3*n)&255));r.wButtons=USHORT(((1u<<(n%12))<<4)|(n%8));r.bTriggerL=BYTE(n);r.bTriggerR=BYTE(255-(n&255));require(VIGEM_SUCCESS(vigem_target_ds4_update(client,target,r)),"ViGEm DS4 submission");}
  }else if(backend=="vdevice"){bool gip=profile=="xbox-one-gip";session.Apply({{"buttons",n%2?4096:8192},{"lx",int(n)},{"ly",-int(n)},{"lt",gip?4*int(n&255)+3:int(n&255)},{"rt",gip?4*(255-int(n&255))+3:255-int(n&255)}});}
  else {XUSB_REPORT r{};r.wButtons=n%2?0x1000:0x2000;r.sThumbLX=SHORT(n);r.sThumbLY=SHORT(-int(n));r.bLeftTrigger=BYTE(n);r.bRightTrigger=BYTE(255-(n&255));require(VIGEM_SUCCESS(vigem_target_x360_update(client,target,r)),"ViGEm state submission");}
  auto returned=qpc();require(WaitForSingleObject(ack.value,5000)==WAIT_OBJECT_0&&channel->ack==LONG(n),"XInput observation deadline");rows.push_back({n,start,returned});
 }
 InterlockedExchange(&channel->stop,1);require(WaitForSingleObject(process.value,10000)==WAIT_OBJECT_0,"Receiver finish");DWORD code=1;require(GetExitCodeProcess(process.value,&code)&&code==0,"Receiver exit");if(cfg.value("filter",std::string("baseline"))!="baseline")require(waitfile(out/"adapter-done.json",15000),"Filter completion deadline");std::ofstream f(out/"xinput-submission.csv");f<<"sequence,submit_qpc,return_qpc\n";for(auto r:rows)f<<r[0]<<','<<r[1]<<','<<r[2]<<'\n';f.close();save(out/"xinput-done.json",{{"status","completed"},{"resources",resources()}});return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
