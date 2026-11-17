#pragma once
#include <windows.h>
#include <psapi.h>
#include "third-party/json.hpp"
#include <filesystem>
#include <fstream>
#include <vector>
#include <stdexcept>
#include <string>
#include <cstdint>
#include <array>
#include <algorithm>
namespace bench {
using json=nlohmann::json;
namespace fs=std::filesystem;
inline void require(bool value,const char* text){if(!value)throw std::runtime_error(std::string(text)+" Win32="+std::to_string(GetLastError()));}
struct Handle {
 HANDLE value=INVALID_HANDLE_VALUE;
 explicit Handle(HANDLE v=INVALID_HANDLE_VALUE):value(v){}
 ~Handle(){if(value && value!=INVALID_HANDLE_VALUE)CloseHandle(value);}
 Handle(const Handle&)=delete;Handle& operator=(const Handle&)=delete;
};
inline int64_t qpc(){LARGE_INTEGER x;require(QueryPerformanceCounter(&x)!=0,"QPC");return x.QuadPart;}
inline int64_t frequency(){LARGE_INTEGER x;require(QueryPerformanceFrequency(&x)!=0,"QPF");return x.QuadPart;}
inline json load(const fs::path& p){Handle f(CreateFileW(p.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr));require(f.value!=INVALID_HANDLE_VALUE,"Open JSON");LARGE_INTEGER size{};require(GetFileSizeEx(f.value,&size)&&size.QuadPart>0&&size.QuadPart<=1048576,"Bounded JSON file");std::string text(size_t(size.QuadPart),'\0');DWORD read=0;require(ReadFile(f.value,text.data(),DWORD(text.size()),&read,nullptr)&&read==text.size(),"Read JSON");return json::parse(text);}
inline void save(const fs::path& p,const json& j){auto tmp=p;tmp+=L".tmp";{std::ofstream f(tmp);require(bool(f),"Write JSON");f<<j.dump(2)<<'\n';f.flush();require(bool(f),"Flush JSON");}require(MoveFileExW(tmp.c_str(),p.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)!=FALSE,"Commit JSON atomically");}
inline bool waitfile(const fs::path& p,unsigned ms){auto end=GetTickCount64()+ms;while(GetTickCount64()<end){if(fs::exists(p))return true;Sleep(10);}return false;}
inline void guard(){require(fs::exists(L"C:\\TitanCSABenchmarkLab\\authorized-lab.json"),"Dedicated lab marker missing");}
inline uint32_t checksum(const uint8_t* p,size_t n){uint32_t x=2166136261u;for(size_t i=0;i<n;++i)x=(x^p[i])*16777619u;return x;}
inline json resources(){FILETIME c,e,k,u;require(GetProcessTimes(GetCurrentProcess(),&c,&e,&k,&u)!=0,"Process times");PROCESS_MEMORY_COUNTERS m{};m.cb=sizeof(m);require(GetProcessMemoryInfo(GetCurrentProcess(),&m,sizeof(m))!=0,"Memory counters");auto ticks=[](FILETIME t){return (uint64_t(t.dwHighDateTime)<<32)|t.dwLowDateTime;};return {{"kernel_100ns",ticks(k)},{"user_100ns",ticks(u)},{"working_set_bytes",m.WorkingSetSize},{"peak_working_set_bytes",m.PeakWorkingSetSize}};}
}
