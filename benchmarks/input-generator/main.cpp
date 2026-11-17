#include "../common/Common.h"
#include "Vdevice.h"
#include <setupapi.h>
#include <hidsdi.h>
#include <cstring>
#include <iostream>
using namespace bench;
Vdevice::Device_Config vendor(const std::string& profile){
 using namespace Vdevice;Device_Config c;c.input_depth=256;
 std::vector<uint8_t> report={0x06,0x00,0xff,0x09,0x01,0xa1,0x01,0x85,0x01,0x09,0x02,0x15,0,0x26,0xff,0,0x75,8,0x95,31,0x81,2,0xc0};
 c.descriptors={
 {Descriptor_Kind::Standard,0,0,0,{18,1,0,2,0,0,0,64,0xff,0xff,0x51,0xb7,0,1,0,0,0,1}},
 {Descriptor_Kind::Standard,0,0,0,{9,2,34,0,1,1,0,0x80,50,9,4,0,0,1,3,0,0,0,9,0x21,0x11,1,0,1,0x22,static_cast<uint8_t>(report.size()),0,7,5,0x81,3,32,0,1}},
 {Descriptor_Kind::Report,0,0,0,report}};
 if(profile!="vendor-hid"){
  require(profile=="mouse"||profile=="keyboard","Unknown profile");bool keyboard=profile=="keyboard";
  c.descriptors[0].data[10]=keyboard?0x53:0x52;
  report=keyboard?std::vector<uint8_t>{0x05,1,0x09,6,0xa1,1,0x05,7,0x19,0xe0,0x29,0xe7,0x15,0,0x25,1,0x75,1,0x95,8,0x81,2,0x95,1,0x75,8,0x81,1,0x95,6,0x75,8,0x15,0,0x25,0x65,0x19,0,0x29,0x65,0x81,0,0xc0}:std::vector<uint8_t>{0x05,1,0x09,2,0xa1,1,0x09,1,0xa1,0,0x05,9,0x19,1,0x29,5,0x15,0,0x25,1,0x95,5,0x75,1,0x81,2,0x95,1,0x75,3,0x81,1,0x05,1,0x09,0x30,0x09,0x31,0x16,0,0x80,0x26,0xff,0x7f,0x75,16,0x95,2,0x81,6,0x09,0x38,0x15,0x81,0x25,0x7f,0x75,8,0x95,1,0x81,6,0xc0,0xc0};
  c.descriptors[1].data[25]=static_cast<uint8_t>(report.size());c.descriptors[2].data=report;
 }
 return c;
}
std::wstring findpath(uint16_t pid){
 GUID guid;HidD_GetHidGuid(&guid);auto set=SetupDiGetClassDevsW(&guid,nullptr,nullptr,DIGCF_PRESENT|DIGCF_DEVICEINTERFACE);require(set!=INVALID_HANDLE_VALUE,"HID enumerate");
 std::wstring result;SP_DEVICE_INTERFACE_DATA item{};item.cbSize=sizeof(item);
 for(DWORD i=0;SetupDiEnumDeviceInterfaces(set,nullptr,&guid,i,&item);++i){
  DWORD size=0;SetupDiGetDeviceInterfaceDetailW(set,&item,nullptr,0,&size,nullptr);if(size<sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA_W))continue;
  std::vector<uint8_t> b(size);auto detail=reinterpret_cast<SP_DEVICE_INTERFACE_DETAIL_DATA_W*>(b.data());detail->cbSize=sizeof(*detail);
  if(!SetupDiGetDeviceInterfaceDetailW(set,&item,detail,size,nullptr,nullptr))continue;
  std::wstring identity=detail->DevicePath;std::transform(identity.begin(),identity.end(),identity.begin(),::towlower);wchar_t expected[40]{};swprintf_s(expected,L"vid_ffff&pid_%04x",unsigned(pid));if(identity.find(expected)!=std::wstring::npos){result=detail->DevicePath;break;}
  Handle f(CreateFileW(detail->DevicePath,0,FILE_SHARE_READ|FILE_SHARE_WRITE,nullptr,OPEN_EXISTING,0,nullptr));if(f.value==INVALID_HANDLE_VALUE)continue;
  HIDD_ATTRIBUTES a{};a.Size=sizeof(a);if(HidD_GetAttributes(f.value,&a)&&a.VendorID==0xffff&&a.ProductID==pid){result=detail->DevicePath;break;}
 }SetupDiDestroyDeviceInfoList(set);return result;
}
int wmain(int argc,wchar_t** argv){fs::path out;try{
 if(argc!=3){std::cerr<<"usage: InputGenerator scenario.json NEW_OUTPUT_DIRECTORY\n";return 2;}guard();auto cfg=load(argv[1]);out=argv[2];require(!fs::exists(out),"Output directory already exists");fs::create_directories(out);
 auto count=cfg.at("samples").get<unsigned>(),warm=cfg.at("warmup").get<unsigned>(),hz=cfg.at("requested_hz").get<unsigned>(),seed=cfg.at("seed").get<uint32_t>();
 require(count>=1&&count<=1000000&&warm<=10000&&hz>=1&&hz<=100000&&uint64_t(count+warm)*1000/hz<=600000,"Bounded scenario");
 auto profile=cfg.value("profile",std::string("vendor-hid"));require(profile=="vendor-hid"||count+warm<30000,"Raw input sequence bounds");
 Handle rawMapping,rawEvent;volatile LONG* rawAck=nullptr;struct Unmap {volatile LONG*& p;~Unmap(){if(p)UnmapViewOfFile(const_cast<LONG*>(p));}}unmap{rawAck};
 if(profile=="mouse"&&cfg.value("closed_loop",false)){auto name=L"Global\\TitanCSABenchmarkRaw-"+std::to_wstring(GetCurrentProcessId())+L"-"+std::to_wstring(GetTickCount64());rawMapping.value=CreateFileMappingW(INVALID_HANDLE_VALUE,nullptr,PAGE_READWRITE,0,sizeof(LONG),name.c_str());require(rawMapping.value!=nullptr,"Raw channel");rawAck=static_cast<LONG*>(MapViewOfFile(rawMapping.value,FILE_MAP_ALL_ACCESS,0,0,sizeof(LONG)));require(rawAck!=nullptr,"Map raw channel");*rawAck=0;rawEvent.value=CreateEventW(nullptr,FALSE,FALSE,(name+L"-ack").c_str());require(rawEvent.value!=nullptr,"Raw ack event");cfg["raw_channel"]=fs::path(name).u8string();}
 auto start=qpc();auto d=Vdevice::Create_Device(vendor(profile));require(bool(d),d.message.c_str());auto created=qpc();std::wstring path;
 for(unsigned i=0;i<300&&path.empty();++i){path=findpath(profile=="mouse"?0xb752:profile=="keyboard"?0xb753:0xb751);if(path.empty())Sleep(50);}require(!path.empty(),"HID enumeration deadline");auto enumerated=qpc();
 cfg["qpc_frequency"]=frequency();cfg["path"]=fs::path(path).u8string();cfg["device_origin"]="virtual";cfg["measurement"]="Vdevice Send_Input entry to independent Windows HID ReadFile completion";cfg["create_ticks"]=created-start;cfg["enumeration_ticks"]=enumerated-start;save(out/"run.json",cfg);
 require(waitfile(out/"receiver-ready.json",30000),"Independent receiver did not become ready");
 std::vector<std::array<int64_t,4>> rows;rows.reserve(count+warm);const auto origin=qpc();const auto freq=frequency();unsigned errors=0;
 Handle timer(CreateWaitableTimerExW(nullptr,nullptr,0x2,TIMER_ALL_ACCESS));if(!timer.value)timer.value=CreateWaitableTimerW(nullptr,TRUE,nullptr);
 for(unsigned n=0;n<count+warm;++n){
  const auto target=origin+int64_t(uint64_t(n)*freq/hz);
  for(;;){auto remaining=target-qpc();if(remaining<=0)break;LARGE_INTEGER due;due.QuadPart=-std::max<int64_t>(1,remaining*10000000/freq);require(SetWaitableTimer(timer.value,&due,0,nullptr,nullptr,FALSE)!=0,"Pacing timer");require(WaitForSingleObject(timer.value,2000)==WAIT_OBJECT_0,"Pacing deadline");}
  std::vector<uint8_t> report(32);report[0]=1;std::memcpy(report.data()+1,&n,4);auto sent=qpc();std::memcpy(report.data()+5,&sent,8);std::memcpy(report.data()+13,&seed,4);for(unsigned i=17;i<28;++i)report[i]=uint8_t((n*37u+i*13u+seed)&255u);auto crc=checksum(report.data(),28);std::memcpy(report.data()+28,&crc,4);
  if(profile=="mouse"){report.assign(6,0);int16_t x=int16_t(n+1),y=int16_t(-x);std::memcpy(report.data()+1,&x,2);std::memcpy(report.data()+3,&y,2);}
  else if(profile=="keyboard"){report.assign(8,0);if(n%2==0)report[2]=(n/2)%2?5:4;}
  auto r=Vdevice::Send_Input(d,0x81,report);auto done=qpc();errors+=!r;rows.push_back({n,sent,done,r.error});
  if(profile=="mouse"&&cfg.value("closed_loop",false)&&!(cfg.value("operation",std::string("forward"))=="block"&&(n+1)%2)){
   require(WaitForSingleObject(rawEvent.value,5000)==WAIT_OBJECT_0&&InterlockedCompareExchange(rawAck,0,0)==LONG(n+1),"Raw Input acknowledgement deadline");
  }
 }
 std::ofstream f(out/"submission.csv");f<<"sequence,submit_qpc,return_qpc,error\n";for(auto r:rows)f<<r[0]<<','<<r[1]<<','<<r[2]<<','<<r[3]<<'\n';f.close();save(out/"generator-done.json",{{"errors",errors},{"resources",resources()}});
 require(waitfile(out/"receiver-done.json",15000),"Receiver completion deadline");if(cfg.value("filter",std::string("baseline"))!="baseline")require(waitfile(out/"adapter-done.json",15000),"Filter completion deadline");auto del=qpc();auto r=Vdevice::Delete_Device(d);require(bool(r),"Delete device");save(out/"lifecycle.json",{{"delete_ticks",qpc()-del},{"clock_pair_overhead_ticks",[](){auto a=qpc();auto b=qpc();return b-a;}()}});return errors?1:0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';if(!out.empty()&&fs::exists(out))save(out/"generator-error.json",{{"error",e.what()}});return 1;}}
