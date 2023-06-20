#include <map>
#include <string>
#include <iostream>
#include<fstream>
#include <set>
#include <sstream>
#include <queue>
#include <locale>
using namespace std;

class XKJDTree {
public:
    string char_or_words;
    string code;
    float freq;
    map<char,vector<XKJDTree*> > childs;
    XKJDTree(string cw_,string code_,float freq_) : char_or_words(cw_),code(code_),freq(freq_) {childs.clear();}
    bool insert(string code_,string cw_,float freq_,int min_depth) {
        string cur_code = "";
        int code_len = code_.length();
        int cur_depth = 0;
        auto cur = this;
        for (int i = 0;i < code_len;i++) {
            char c = code_[i];
            cur_code = cur_code + c;
            cur_depth += 1;
            if (cur->char_or_words == cw_)
                return true;
            if (cur->childs.find(c) == cur->childs.end()) {
                if (cur_depth >= min_depth) {
                    cur->childs[c].push_back(new XKJDTree(cw_,cur_code,freq_));
                    return true;
                } else {
                    cur->childs[c].push_back(new XKJDTree("","",-1));
                    cur = cur->childs[c][0];
                }
            } else {
                if (i + 1 == code_len) {
                    for (auto& child : cur->childs[c]) {
                        if (child->char_or_words == cw_ and child->code == cur_code)
                            return true;
                    }
                    if (code_len == 2 || code_len == 3)
                        return false;
                    cur->childs[c].push_back(new XKJDTree(cw_,cur_code,freq_));
                    return true;
                } else {
                    if (cur->childs[c][0]->char_or_words == "" && cur_depth >= min_depth) {
                        cur = cur->childs[c][0];
                        cur->char_or_words = cw_;
                        cur->code = cur_code;
                        cur->freq = freq_;
                        return true;
                    }
                    cur = cur->childs[c][0];
                }
            }
        }
        return false;
    }
};

int utf8_strlen(const string& str)
{
    int c,i,ix,q;
    for (q=0, i=0, ix=str.length(); i < ix; i++, q++)
    {
        c = (unsigned char) str[i];
        if      (c>=0   && c<=127) i+=0;
        else if ((c & 0xE0) == 0xC0) i+=1;
        else if ((c & 0xF0) == 0xE0) i+=2;
        else if ((c & 0xF8) == 0xF0) i+=3;
        //else if (($c & 0xFC) == 0xF8) i+=4; // 111110bb //byte 5, unnecessary in 4 byte UTF-8
        //else if (($c & 0xFE) == 0xFC) i+=5; // 1111110b //byte 6, unnecessary in 4 byte UTF-8
        else return 0;//invalid utf8
    }
    return q;
}
vector<string> split_to_char(const string& str) {
    int c,i,ix,q;
    vector<string> ans;
    for (q=0, i=0, ix=str.length(); i < ix; i++, q++)
    {
        c = (unsigned char) str[i];
        if      (c>=0   && c<=127) {
            ans.push_back(str.substr(i,1));
            i+=0;
        }
        else if ((c & 0xE0) == 0xC0) {
            ans.push_back(str.substr(i,2));
            i+=1;
        }
        else if ((c & 0xF0) == 0xE0) {
            ans.push_back(str.substr(i,3));
            i+=2;
        }
        else if ((c & 0xF8) == 0xF0) {
            ans.push_back(str.substr(i,4));
            i+=3;
        }
        //else if (($c & 0xFC) == 0xF8) i+=4; // 111110bb //byte 5, unnecessary in 4 byte UTF-8
        //else if (($c & 0xFE) == 0xFC) i+=5; // 1111110b //byte 6, unnecessary in 4 byte UTF-8
        else return ans;//invalid utf8
    }
    return ans;
}
vector<string> pinyin_split(const string& pinyin) {
    vector<string> ans;
    stringstream ss(pinyin);
    string word;
    while (ss >> word) {
        ans.push_back(word);
    }
    return ans;
}

map<string,string> PY_TO_JD = {
{"wai","wh"},
{"bang","bp"},
{"nan","nf"},
{"die","dd"},
{"liao","lc"},
{"sou","sd"},
{"chuo","wl"},
{"ma","ms"},
{"lang","lp"},
{"zhuo","fl"},
{"cou","cd"},
{"xiong","xy"},
{"tou","td"},
{"han","hf"},
{"rua","rq"},
{"zai","zh"},
{"dui","db"},
{"lian","lm"},
{"sen","sn"},
{"feng","fr"},
{"nuan","nt"},
{"zhuai","fg"},
{"lao","lz"},
{"nong","ny"},
{"guai","gg"},
{"ei","xw"},
{"man","mf"},
{"tui","tb"},
{"yuan","yt"},
{"hou","hd"},
{"xi","xk"},
{"shu","ej"},
{"zhu","fj"},
{"can","cf"},
{"ying","yg"},
{"e","xe"},
{"ti","tk"},
{"piao","pc"},
{"tong","ty"},
{"song","sy"},
{"sui","sb"},
{"zeng","zr"},
{"zhao","qz"},
{"ruan","rt"},
{"zan","zf"},
{"dai","dh"},
{"reng","rr"},
{"nou","nd"},
{"jie","jd"},
{"neng","nr"},
{"hai","hh"},
{"yang","yp"},
{"shuai","eg"},
{"jue","jh"},
{"duo","dl"},
{"cuan","ct"},
{"me","me"},
{"nve","nh"},
{"nue","nh"},
{"dao","dz"},
{"cu","cj"},
{"kui","kb"},
{"gu","gj"},
{"kang","kp"},
{"yo","yl"},
{"yue","yh"},
{"kuang","kx"},
{"jing","jg"},
{"cuo","cl"},
{"du","dj"},
{"biao","bc"},
{"nuo","nl"},
{"yun","yw"},
{"hao","hz"},
{"sun","sw"},
{"sa","ss"},
{"wo","wl"},
{"huai","hg"},
{"chui","wb"},
{"cen","cn"},
{"su","sj"},
{"lan","lf"},
{"yin","yb"},
{"qian","qm"},
{"rang","rp"},
{"den","dn"},
{"tao","tz"},
{"bing","bg"},
{"cang","cp"},
{"tan","tf"},
{"teng","tr"},
{"chang","jp"},
{"lie","ld"},
{"ming","mg"},
{"pan","pf"},
{"mi","mk"},
{"jiao","jc"},
{"shuan","et"},
{"pen","pn"},
{"zei","zw"},
{"chuang","wx"},
{"gao","gz"},
{"fou","fd"},
{"kou","kd"},
{"ning","ng"},
{"zhui","fb"},
{"chou","jd"},
{"wa","ws"},
{"er","xj"},
{"he","he"},
{"dang","dp"},
{"ta","ts"},
{"geng","gr"},
{"pang","pp"},
{"dong","dy"},
{"shuo","el"},
{"chai","jh"},
{"ba","bs"},
{"zen","zn"},
{"bo","bl"},
{"dan","df"},
{"kuan","kt"},
{"pa","ps"},
{"xia","xs"},
{"xue","xh"},
{"gong","gy"},
{"rao","rz"},
{"long","ly"},
{"lai","lh"},
{"eng","xr"},
{"huo","hl"},
{"kua","kq"},
{"qiong","qy"},
{"pai","ph"},
{"qing","qg"},
{"kuai","kg"},
{"lv","ll"},
{"kan","kf"},
{"ao","xz"},
{"fang","fp"},
{"mian","mm"},
{"miu","mq"},
{"fei","fw"},
{"shei","ew"},
{"an","xf"},
{"lo","ll"},
{"kao","kz"},
{"zhan","qf"},
{"xin","xb"},
{"zhou","qd"},
{"bao","bz"},
{"beng","br"},
{"guang","gx"},
{"chen","jn"},
{"gua","gq"},
{"kong","ky"},
{"ai","xh"},
{"zhuan","ft"},
{"en","xn"},
{"ken","kn"},
{"kuo","kl"},
{"zhua","fq"},
{"ye","ye"},
{"diu","dq"},
{"cha","js"},
{"mou","md"},
{"dou","dd"},
{"gan","gf"},
{"shi","ek"},
{"mai","mh"},
{"nen","nn"},
{"po","pl"},
{"jia","js"},
{"nai","nh"},
{"cong","cy"},
{"shan","ef"},
{"li","lk"},
{"ya","ys"},
{"chuai","wg"},
{"che","je"},
{"cui","cb"},
{"pao","pz"},
{"ding","dg"},
{"bai","bh"},
{"xv","xl"},
{"ri","rk"},
{"hang","hp"},
{"hei","hw"},
{"keng","kr"},
{"dia","ds"},
{"mie","md"},
{"sheng","er"},
{"zhun","fw"},
{"shao","ez"},
{"leng","lr"},
{"luo","ll"},
{"ku","kj"},
{"pin","pb"},
{"jiu","jq"},
{"pu","pj"},
{"nv","nl"},
{"gen","gn"},
{"you","yd"},
{"le","le"},
{"nin","nb"},
{"qi","qk"},
{"cheng","jr"},
{"jiong","jy"},
{"ke","ke"},
{"ne","ne"},
{"dian","dm"},
{"si","sk"},
{"ca","cs"},
{"pian","pm"},
{"zheng","qr"},
{"nang","np"},
{"lia","ls"},
{"hua","hq"},
{"ga","gs"},
{"mo","ml"},
{"chi","wk"},
{"huang","hx"},
{"zhong","qy"},
{"bei","bw"},
{"ci","ck"},
{"jian","jm"},
{"na","ns"},
{"deng","dr"},
{"wang","wp"},
{"qie","qd"},
{"gui","gb"},
{"o","xl"},
{"niang","nx"},
{"kai","kh"},
{"bu","bj"},
{"ran","rf"},
{"zang","zp"},
{"di","dk"},
{"kun","kw"},
{"shuang","ex"},
{"fen","fn"},
{"zi","zk"},
{"cai","ch"},
{"ji","jk"},
{"se","se"},
{"chuan","wt"},
{"fan","ff"},
{"wu","wj"},
{"tuo","tl"},
{"hen","hn"},
{"zhuang","fx"},
{"cao","cz"},
{"fa","fs"},
{"nian","nm"},
{"wan","wf"},
{"dei","dw"},
{"pi","pk"},
{"shou","ed"},
{"tang","tp"},
{"chua","wq"},
{"tai","th"},
{"xiu","xq"},
{"zhi","fk"},
{"mu","mj"},
{"tun","tw"},
{"duan","dt"},
{"nao","nz"},
{"qiang","qx"},
{"mang","mp"},
{"xie","xd"},
{"fo","fl"},
{"chan","jf"},
{"sha","es"},
{"yi","yk"},
{"sai","sh"},
{"sang","sp"},
{"lei","lw"},
{"tiao","tc"},
{"lin","lb"},
{"dun","dw"},
{"quan","qt"},
{"hui","hb"},
{"gei","gw"},
{"te","te"},
{"yao","yz"},
{"ceng","cr"},
{"zhai","qh"},
{"heng","hr"},
{"de","de"},
{"chun","ww"},
{"shen","en"},
{"ling","lg"},
{"lve","lh"},
{"lue","lh"},
{"huan","ht"},
{"ze","ze"},
{"xun","xw"},
{"bie","bd"},
{"zun","zw"},
{"ping","pg"},
{"she","ee"},
{"yan","yf"},
{"seng","sr"},
{"gou","gd"},
{"rou","rd"},
{"zou","zd"},
{"gun","gw"},
{"fu","fj"},
{"tuan","tt"},
{"ban","bf"},
{"gang","gp"},
{"qun","qw"},
{"xiang","xx"},
{"zhang","qp"},
{"ha","hs"},
{"guan","gt"},
{"ang","xp"},
{"lu","lj"},
{"wei","ww"},
{"wen","wn"},
{"kei","kw"},
{"juan","jt"},
{"xiao","xc"},
{"zao","zz"},
{"shua","eq"},
{"jun","jw"},
{"min","mb"},
{"miao","mc"},
{"shang","ep"},
{"hun","hw"},
{"mao","mz"},
{"da","ds"},
{"ou","xd"},
{"jin","jb"},
{"shun","ew"},
{"chao","jz"},
{"diao","dc"},
{"ben","bn"},
{"tie","td"},
{"peng","pr"},
{"ni","nk"},
{"sao","sz"},
{"zhe","qe"},
{"ting","tg"},
{"qia","qs"},
{"a","xs"},
{"meng","mr"},
{"yu","yj"},
{"qin","qb"},
{"tian","tm"},
{"niao","nc"},
{"que","qh"},
{"zui","zb"},
{"chong","jy"},
{"zhei","qw"},
{"zong","zy"},
{"rong","ry"},
{"qv","ql"},
{"nie","nd"},
{"jv","jl"},
{"ru","rj"},
{"ruo","rl"},
{"re","re"},
{"pei","pw"},
{"la","ls"},
{"yong","yy"},
{"fiao","fc"},
{"xuan","xt"},
{"qiao","qc"},
{"nu","nj"},
{"zu","zj"},
{"cun","cw"},
{"ge","ge"},
{"suo","sl"},
{"nun","nw"},
{"hong","hy"},
{"chu","wj"},
{"guo","gl"},
{"liu","lq"},
{"mei","mw"},
{"nei","nw"},
{"bi","bk"},
{"za","zs"},
{"hu","hj"},
{"lou","ld"},
{"luan","lt"},
{"xian","xm"},
{"biang","bx"},
{"bian","bm"},
{"suan","st"},
{"lun","lw"},
{"weng","wr"},
{"zuo","zl"},
{"rui","rb"},
{"zha","qs"},
{"liang","lx"},
{"jiang","jx"},
{"pou","pd"},
{"san","sf"},
{"ce","ce"},
{"gai","gh"},
{"xing","xg"},
{"men","mn"},
{"niu","nq"},
{"tu","tj"},
{"run","rw"},
{"shui","eb"},
{"shai","eh"},
{"ren","rn"},
{"ka","ks"},
{"pie","pd"},
{"zuan","zt"},
{"zhen","qn"},
{"bin","bb"},
{"qiu","qq"},
{"n","xn"},
{"xu","xl"},
{"ju","jl"},
{"qu","ql"},
{"m","mj"},
{"ng","xn"},

};

void get_final_dict(XKJDTree* now,ofstream& rfs) {
    if (now->code != "" && now->char_or_words != "") {
        rfs << now->char_or_words << "\t" << now->code << "\t" << now->freq << endl;
    }
    for (auto im : now->childs){
        for (auto child : im.second)
            get_final_dict(child,rfs);
    }
}
int main() {
    ifstream  fin;
    map<string,string> danzi_bihua_dict;
    set<string> JD_PY;
    for (auto & im : PY_TO_JD){
        JD_PY.insert(im.second);
    }
    ifstream danziin;
    char buf[4096];
    danziin.open("/Users/chenkailong/myOperSource/xkjd_opt/data/src/xkjd6/xkjd6.danzi.final.txt",ios::in);
    while (danziin.getline(buf,sizeof(buf))) {
        int i = 0;
        string cw;
        for (i = 0;buf[i] != '\t';i++) {
            cw = cw + buf[i];
        }
        i++;
        string code;
        for (;buf[i] != '\t';i++)
            code = code + buf[i];
        danzi_bihua_dict[cw] = code.substr(2);
    }
    cout << danzi_bihua_dict.size() << endl;
    fin.open("/Users/chenkailong/myOperSource/xkjd_opt/data/hongyan_pinyin/merged.all.dict.yaml",ios::in);

    XKJDTree rt("","",-1);
    int cnt = 0;
    int fail_cnt = 0;
    int sum_cnt = 0;
    while (fin.getline(buf,sizeof(buf))) {
        sum_cnt++;
        int i;
        string cw;
        for (i = 0;buf[i] != '\t';i++) {
            cw = cw + buf[i];
        }
        vector<string> single_char  = split_to_char(cw);
        i++;
        string pinyin;
        for (;buf[i] != '\t';i++)
            pinyin = pinyin + buf[i];
        auto pinyin_sp = pinyin_split(pinyin);
        float weight = stof(buf + i);
        int word_len = utf8_strlen(cw);
        if (word_len == 1) {
            if (danzi_bihua_dict.find(cw) == danzi_bihua_dict.end()) {
                fail_cnt++;
                continue;
            }
            string jd_py = PY_TO_JD[pinyin];
            string code = jd_py + danzi_bihua_dict[cw];
            if (rt.insert(code,cw,weight,word_len)) {
                cnt++;
                continue;
            }
            fail_cnt++;
        } else if (word_len == 2) {
            if (danzi_bihua_dict.find(single_char[0]) == danzi_bihua_dict.end()) {
                fail_cnt++;
                continue;
            }
            if (danzi_bihua_dict.find(single_char[1]) == danzi_bihua_dict.end()) {
                fail_cnt++;
                continue;
            }


            string short_pinyin = string() + PY_TO_JD[pinyin_sp[0]][0] + PY_TO_JD[pinyin_sp[1]][0];
            if ( JD_PY.count(short_pinyin) == 0 and rt.insert(
                short_pinyin, cw, weight, 2
            )){
                cnt++;
                continue;
            }

            string short_code = string() + PY_TO_JD[pinyin_sp[0]][0] + danzi_bihua_dict[single_char[1]].substr(0,2);
            if (  rt.insert(
                short_code, cw, weight, 2
            )){
                cnt++;
                continue;
            }
            string code = PY_TO_JD[pinyin_sp[0]] +   PY_TO_JD[pinyin_sp[1]] + danzi_bihua_dict[single_char[0]].substr(0,2) + danzi_bihua_dict[single_char[1]].substr(0,2);
            if (  rt.insert(
                code, cw, weight, 2
            )) {
                cnt++;
                continue;
            }

            fail_cnt++;
        } else {
            string code_py = "";
            string code_bihua = "";
            bool find_fail = false;
            for (int j = 0;j < pinyin_sp.size();j++) {
                if (danzi_bihua_dict.find(single_char[j]) == danzi_bihua_dict.end()) {
                    find_fail = true;
                    fail_cnt++;
                    break;
                }
                code_py = code_py + PY_TO_JD[pinyin_sp[j]][0];
                code_bihua = code_bihua + danzi_bihua_dict[single_char[j]].substr(0,2);
            }
            if (find_fail) {
                continue;
            }
            string code = code_py + code_bihua;
            if (rt.insert(code, cw, weight, word_len)){
                cnt++;
            } else {
                fail_cnt++;
            }
        }

    }
    cout << "sum " << sum_cnt << endl;
    cout << "fail " << fail_cnt << endl;
    cout << "OK " << cnt << endl;
    ofstream rfs("/Users/chenkailong/myOperSource/xkjd_opt/results/xkjd6/xkjd6.hongyan.dict.yaml");
    get_final_dict(&rt,rfs);
    return 0;
}
