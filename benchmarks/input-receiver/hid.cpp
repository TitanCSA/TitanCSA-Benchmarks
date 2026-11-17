// Independent receiver: Windows HID/ReadFile only; never links a vendor SDK.
#include "../common/Common.h"
#include <hidsdi.h>
#include <hidpi.h>
#include <cstring>
#include <iostream>
using namespace bench;
int wmain(int argc,wchar_t** argv){fs::path out;try{
 if(argc!=2)return 2;guard();out=argv[1];require(waitfile(out/"run.json",45000),"Generator enumeration deadline");auto cfg=load(out/"run.json");auto path=fs::u8path(cfg.at("path").get<std::string>());
 require(cfg.at("qpc_frequency").get<int64_t>()==frequency(),"QPC domain mismatch");
 Handle file(CreateFileW(path.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE,nullptr,OPEN_EXISTING,FILE_FLAG_OVERLAPPED,nullptr));require(file.value!=INVALID_HANDLE_VALUE,"Open benchmark HID collection");
 PHIDP_PREPARSED_DATA data=nullptr;require(HidD_GetPreparsedData(file.value,&data)!=FALSE,"HID descriptor");HIDP_CAPS caps{};auto status=HidP_GetCaps(data,&caps);HidD_FreePreparsedData(data);require(status==HIDP_STATUS_SUCCESS&&caps.InputReportByteLength==32&&caps.UsagePage==0xff00,"Expected vendor HID descriptor");require(HidD_SetNumInputBuffers(file.value,512)!=FALSE,"HID input buffering");
 Handle event(CreateEventW(nullptr,TRUE,FALSE,nullptr));require(event.value!=nullptr,"Read event");std::vector<std::array<int64_t,4>> rows;auto total=cfg.at("samples").get<unsigned>()+cfg.at("warmup").get<unsigned>();rows.reserve(total);save(out/"receiver-ready.json",{{"api","Windows HID ReadFile"},{"input_report_bytes",caps.InputReportByteLength},{"qpc_frequency",frequency()}});
 const auto deadline=GetTickCount64()+650000;unsigned idle=0;
 while(rows.size()<total&&GetTickCount64()<deadline){
  std::array<uint8_t,32> b{};OVERLAPPED ov{};ov.hEvent=event.value;ResetEvent(event.value);DWORD count=0;auto ok=ReadFile(file.value,b.data(),DWORD(b.size()),&count,&ov);auto err=ok?ERROR_SUCCESS:GetLastError();require(ok||err==ERROR_IO_PENDING,"HID read");
  if(!ok&&WaitForSingleObject(event.value,1000)!=WAIT_OBJECT_0){CancelIoEx(file.value,&ov);GetOverlappedResult(file.value,&ov,&count,TRUE);if(fs::exists(out/"generator-done.json")&&++idle>=3)break;continue;}
  require(GetOverlappedResult(file.value,&ov,&count,FALSE)!=FALSE,"Read result");auto received=qpc();uint32_t seq=0,seed=0,crc=0;int64_t sent=0;std::memcpy(&seq,b.data()+1,4);std::memcpy(&sent,b.data()+5,8);std::memcpy(&seed,b.data()+13,4);std::memcpy(&crc,b.data()+28,4);bool valid=count==32&&b[0]==1&&seed==cfg.at("seed").get<uint32_t>()&&crc==checksum(b.data(),28)&&seq<total&&sent<=received;for(unsigned i=17;i<28;++i)valid=valid&&b[i]==uint8_t((seq*37u+i*13u+seed)&255u);rows.push_back({seq,sent,received,valid?1:0});
 }
 std::ofstream f(out/"reception.csv");f<<"sequence,submit_qpc,receive_qpc,content_valid\n";for(auto r:rows)f<<r[0]<<','<<r[1]<<','<<r[2]<<','<<r[3]<<'\n';f.close();save(out/"receiver-done.json",{{"received",rows.size()},{"resources",resources()}});return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';if(!out.empty()&&fs::exists(out))save(out/"receiver-error.json",{{"error",e.what()}});return 1;}}
