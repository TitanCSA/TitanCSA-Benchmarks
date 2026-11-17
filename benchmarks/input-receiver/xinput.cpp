#include "../common/XInputChannel.h"
#include <Xinput.h>
#include <iostream>
using namespace bench;
int wmain(int argc,wchar_t** argv){try{
 if(argc!=3)return 2;guard();fs::path out=argv[1];std::wstring name=argv[2];
 auto cfg=load(out/"xinput-run.json");bool modified=cfg.value("operation",std::string("forward"))=="modify";
 Handle mapping(OpenFileMappingW(FILE_MAP_ALL_ACCESS,FALSE,name.c_str()));require(mapping.value!=nullptr,"Open measurement mapping");auto* channel=static_cast<XInputChannel*>(MapViewOfFile(mapping.value,FILE_MAP_ALL_ACCESS,0,0,sizeof(XInputChannel)));require(channel!=nullptr,"Map channel");
 Handle event(OpenEventW(EVENT_MODIFY_STATE,FALSE,(name+L"-ack").c_str()));require(event.value!=nullptr,"Open ack event");
 DWORD slot=4,found=0;const auto enumerationEnd=GetTickCount64()+25000;do{found=0;for(DWORD i=0;i<4;++i){XINPUT_STATE s{};if(XInputGetState(i,&s)==ERROR_SUCCESS){slot=i;++found;}}if(found==1)break;require(found<2,"Unrelated XInput controller present");Sleep(50);}while(GetTickCount64()<enumerationEnd);require(found==1,"Exactly one test XInput controller required");
 std::vector<std::array<int64_t,3>> rows;rows.reserve(20000);uint64_t polls=0;InterlockedExchange(&channel->ready,1);const auto end=GetTickCount64()+120000;
 while(!InterlockedCompareExchange(&channel->stop,0,0)&&GetTickCount64()<end){
  XINPUT_STATE state{};auto status=XInputGetState(slot,&state);auto now=qpc();++polls;
  LONG wanted=InterlockedCompareExchange(&channel->expected,0,0);
  if(status==ERROR_SUCCESS&&wanted>0&&state.Gamepad.sThumbLX==wanted&&state.Gamepad.sThumbLY==-wanted&&state.Gamepad.bLeftTrigger==uint8_t(wanted)&&state.Gamepad.bRightTrigger==uint8_t(255-(wanted&255))&&state.Gamepad.wButtons==((wanted%2)?(modified?XINPUT_GAMEPAD_X:XINPUT_GAMEPAD_A):(modified?XINPUT_GAMEPAD_Y:XINPUT_GAMEPAD_B))&&InterlockedCompareExchange(&channel->ack,0,0)!=wanted){
   rows.push_back({wanted,channel->sent,now});InterlockedExchange(&channel->ack,wanted);SetEvent(event.value);
  }else Sleep(0);
 }
 std::ofstream f(out/"xinput-reception.csv");f<<"sequence,submit_qpc,receive_qpc\n";for(auto r:rows)f<<r[0]<<','<<r[1]<<','<<r[2]<<'\n';f.close();save(out/"xinput-receiver.json",{{"received",rows.size()},{"poll_calls",polls},{"slot",slot},{"resources",resources()}});UnmapViewOfFile(channel);return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
