#include "Common.h"
#include "Interceptor.h"
#include <iostream>
using namespace bench;
int wmain(int argc,wchar_t** argv){fs::path out;try{if(argc!=2)return 2;guard();out=argv[1];auto cfg=load(out/(fs::exists(out/"run.json")?"run.json":"xinput-run.json"));auto mode=cfg.value("operation",std::string("forward"));require(mode=="forward"||mode=="modify"||mode=="block","Unknown operation");auto init=Interceptor::Init_AllDevices();save(out/"adapter-init.json",{{"ready",init.ready},{"error",init.error},{"associated",init.associated},{"already_associated",init.already_associated},{"skipped",init.skipped},{"reboot_required",init.reboot_required}});require(init.ready,"Initialize supported devices");{auto first=Interceptor::Get_Input_With_Timeout(0);auto r=Interceptor::Send_Input(first);require(bool(r),"Forward initial batch");}
 save(out/"adapter-ready.json",{{"ready",true}});uint64_t captured=0,blocked=0,modified=0;std::vector<std::array<int64_t,3>> timing;const auto end=GetTickCount64()+180000;
 while(!fs::exists(out/"receiver-done.json")&&!fs::exists(out/"xinput-receiver.json")&&GetTickCount64()<end){auto inputs=Interceptor::Get_Input_With_Timeout(100);auto start=qpc();unsigned count=0;
  for(auto& input:inputs){
#if IC_PRODUCT_HAS_KEYBOARD_MOUSE
   if(input.device_info&&input.device_info->vid==0xffff&&(input.device_info->pid==0xb752||input.device_info->pid==0xb753)){++captured;++count;if(auto* mouse=input.Get<Interceptor::Mouse_Input>()){if(mode=="modify"){mouse->stroke.x=-mouse->stroke.x;++modified;}else if(mode=="block"&&mouse->stroke.x%2){input.blocked=true;++blocked;}}}
#endif
#if IC_PRODUCT_HAS_CONTROLLERS
   if(auto* pad=input.Get<Interceptor::Controller_Xinput_Input>()){if(input.device_info&&input.device_info->vid==0x045e&&input.device_info->pid==0x028e&&pad->state.left_x>0){++captured;++count;if(mode=="modify"){pad->state.buttons=pad->state.buttons==0x1000?0x4000:0x8000;++modified;}}}
   if(input.device_info&&input.device_info->vid==0x054c&&input.device_info->pid==0x05c4){if(auto* hid=input.Get<Interceptor::Controller_Hid_Input>()){if(hid->length>=10&&hid->report[0]==1&&unsigned(hid->report[1])+hid->report[2]==255&&unsigned(hid->report[3])+hid->report[4]==255&&hid->report[8]==hid->report[1]&&hid->report[9]==hid->report[2]){++captured;++count;if(mode=="modify"){hid->report[5]^=0xf0;++modified;}}}}
   Interceptor::Controller_GIP_Input* gip=input.Get<Interceptor::Controller_GIP_Input>();if(auto* raw=input.Get<Interceptor::Controller_GIP_Raw_Input>())gip=&raw->input;
   if(gip&&gip->state.left_x>0&&!fs::exists(out/"first-gip.json"))save(out/"first-gip.json",{{"vid",input.device_info?input.device_info->vid:0},{"pid",input.device_info?input.device_info->pid:0},{"buttons",gip->state.buttons},{"lx",gip->state.left_x},{"ly",gip->state.left_y},{"lt",gip->state.left_trigger},{"rt",gip->state.right_trigger}});
   if(gip&&input.device_info&&(input.device_info->vid==0x045e||(input.device_info->vid==0xffff&&input.device_info->pid==4))&&gip->state.left_x>0){++captured;++count;if(mode=="modify"){gip->state.buttons=gip->state.buttons==0x10?0x40:0x80;++modified;}}
#endif
  }
  auto sent=Interceptor::Send_Input(inputs);require(bool(sent),"Forward captured batch");if(count)timing.push_back({count,start,qpc()});
 }
 Interceptor::Destroy_Context();std::ofstream f(out/"adapter.csv");f<<"captured_count,start_qpc,return_qpc\n";for(auto r:timing)f<<r[0]<<','<<r[1]<<','<<r[2]<<'\n';f.close();save(out/"adapter-done.json",{{"captured",captured},{"blocked",blocked},{"modified",modified},{"resources",resources()}});return captured?0:1;
 }catch(const std::exception& e){std::cerr<<e.what()<<'\n';if(!out.empty()&&fs::exists(out))save(out/"adapter-error.json",{{"error",e.what()}});return 1;}}
