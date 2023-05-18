#include<iostream>
#include<vector>
#include<unordered_set>
#include<fstream>
#include<sstream>
#include<ctime>
#include<cstdlib>
#include<string>
#include<random>
#include<algorithm>




#include<unordered_map>
#include<queue>
#include<chrono>
#include<thread>

using namespace std;

#define numfiles 10
#define interfer 0.7        // giao thoa follower 
#define amp 0.5             // biên độ price
//#define ratioH 0.8           // tỉ trọng Heristic
#define partial  0.3        // thiên vị số lượng follower
#define seedFollower 80    
#define learning_rate 0.005;     

struct Input{
    int numFamous;    
    int fund;  
    vector<int> ids;
    vector<int> price;
    vector<vector<int>> followers;

    Input(){};
    Input(string filename){
        Docfile(filename);
        //printData(filename);
    }

    void Docfile(string filename){
        clearInput();                     // xóa dữ liệu trước khi đọc file mới 
        ifstream file(filename);
        if (file.is_open()) {
        // Đọc dữ liệu từ file
            file >> fund;
            //cout << "fund: " << fund << endl;
            file >> numFamous;
           // cout << "numFamous: " << numFamous << endl;
            string line;
            istringstream ss(line);
            getline(file,line);
            while(getline(file,line)){
                istringstream iss(line);                // đọc tới cuối file
                int id;
                float money;
                iss >> id;
                //cout << "id :" << id  << " " ;
                iss >> money;
                //cout << "price: " << money <<" " << endl;
                vector<int> follow;
                ids.push_back(id);
                price.push_back(money);
                int f;
                while (iss >> f) {
                    //cout << "f: " << f;
                    follow.push_back(f);
                }
                followers.push_back(follow);
            }
            file.close();                   
        }
        else cout << "Unable to open file";
    }
    void clearInput(){
        this->numFamous = 0;
        this->ids.clear();
        //cout << "clear ids :"<< ids.size() <<endl;
        this->price.clear();
        for(auto& follow : this->followers){
            follow.clear();
        }
        this->followers.clear();
    }
    void Display(){
        cout << "NumFamous: " << numFamous << endl;
        cout << "Total money: " << fund << endl;
        for (auto i : ids) {
            cout << "ID: " << i << ", price: " << price[i-1] << ", Followers: ";
            for (int j = 0; j < followers[i].size(); j++) {
                cout << followers[i].size() << ", Followers: ";
                cout << followers[i][j] << " ";
            }
            cout << endl;
        }
    }


};

// NOTE : rand() của ide c++ visual ko thể tạo số ngẫu nhiên quá lớn ( cỡ >100000) , tb_money thuê 1 Famous buộc phải bị giảm xuống 
void Tao1File(string filename){ 
    int numFamous = rand()%101+100;                     // khởi tạo số người nổi tiếng ngẫu nhiên từ 100-200
    long fund = rand()%8000001 + 2000000;              // Khởi tạo tổng số tiền được cấp từ 20.000.000 - 100.000.000
    fund = (fund / 1000) * 1000;                      // làm tròn tới hàng nghìn
    vector<int> ids;
    vector<int> price;
    vector<vector<int>> followers;        
    //float interfer = 0.5 ;                     // giao thoa : có khoảng 50% follower theo dõi hơn 2 người nổi tiếng 
                                                // hoặc 2 Famous sẽ trùng nhau khoảng 50% follower
    float tb = fund/numFamous;                 // trung bình số tiền được cấp trên mỗi người nổi tiếng
    int MaxNumFollowers = numFamous*seedFollower*(1+partial/2);   // Tổng số followers trong data (dự đoán)
    //float amp = 0.5;    // tỉ lệ dao động cho phép giữa tiền thuê và tiền thuê trung bình trong lúc tạo ngẫu nhiên 
                         // (1+amp)/min(tile) phải nhỏ hơn 1 . ví dụ : 1.5/2 = 0.75 , tránh t/h tệ nhất ngẫu nhiên sinh ra thuê hết
                        // người nổi tiếng mà chưa hết tiền
    // Mỗi file data sẽ có 1 tỉ lệ riêng
    float tile = ((float) rand() / RAND_MAX)*2.5 + 2;    //tỉ lệ tiền thuê mỗi người / số tiền trung bình (2.4.5)
                                                        //ví dụ : tỉ lệ là 2 : chỉ đủ tiền để chọn được khoảng 50% số người nổi tiếng 
    int tb_money = (int)tile * tb;                     // tiền thuê trung bình 1 người nổi tiếng
    // Tạo dữ liệu ngẫu nhiên cho mỗi người nổi tiếng
    for (int i = 0; i < numFamous; i++) {    
        int id = i + 1;                                                                                                                          
        int money = rand()%tb_money + amp*tb_money;      // số tiền thuê dao động từ 0.5 . 1.5 số tiền trung bình (tb_money): maxPrice= 3*minPrice 
        money = (money / 1000) * 1000;                  // làm tròn
        price.push_back(money);
        ids.push_back(id); 
        vector<int> follow; 
        float balance =(float) money / tb_money;       //chỉ số tránh thiên vị sinh ra do ngẫu nhiên : giá thuê quá cao nhưng quá ít follower 
        //cout << "balance: " << balance << endl;     // balance dao động trong khoảng (amp ,1+amp)
        int StandNumFollower = balance * seedFollower;
        // khởi tạo số follower của 1 Famous từ 40 -> 144 ( với seed = 80)
        int numFollowers = StandNumFollower + rand()%(int)(StandNumFollower * partial) ; 
        // nếu balance = 0.5 ~ 40 , nếu balance = 1.5 ~ 120
        while(numFollowers>0) {                        // Chọn ngẫu nhiên người theo dõi
            int f = rand() % MaxNumFollowers*(1-interfer/2) + 1;               // chọn ngẫu nhiên follower trong miền giao thoa
            if(find(follow.begin(),follow.end(),f) == follow.end()){          // ktra xem đã xuất hiện trong danh sach theo dõi chưa
                follow.push_back(f);  
                numFollowers--;
            }
        }
        followers.push_back(follow);
    }
    // Tạo file và ghi dữ liệu vào file
    ofstream file(filename);
    if (file.is_open()) {
        file << fund << endl;                   // dòng đầu tiên là tổng số tiền
        file << numFamous << endl;              // dòng 2 là số người nổi tiếng 
        for (int i = 0; i < numFamous; i++) {
            file << ids[i] << " " << price[i] << " ";
            for (int j = 0; j < followers[i].size(); j++) {
                file << followers[i][j] << " ";
            }
            file << endl;
        }
        file.close();
    }
    else{
    cout << "Cannot write into file !" << endl;
    }
}

void TaoNhieuFile(){
    for(int i=1; i<=numfiles; i++){
        string filename = "dataIM" + to_string(i) + ".txt";
        Tao1File(filename);
    }

}

void printData(string filename){
    int numFamous;                  
    int fund;                        
    vector<int> ids;
    vector<int> price;
    vector<vector<int>> followers;
    ifstream file(filename);
    if (file.is_open()) {
    // Đọc dữ liệu từ file
        file >> fund;
        file >> numFamous;
        string line;
        istringstream ss(line);
        getline(file,line);
        while(getline(file,line)){
            istringstream iss(line);             
            int id;
            float money;
            iss >> id;
            //cout << " id: " << id;
            iss >> money;
            vector<int> follow;
            // file >> id >> money;
            ids.push_back(id);
            //numFamous++;                   // tính numFamous
            price.push_back(money);
            int f;
            while (iss >> f) {            // đọc liên tiếp các follower của 1 ng nổi tiếng 
                follow.push_back(f);;
            }
            //cout<< "ids.size(): " << ids.size() << endl;
            followers.push_back(follow);
        }
    // In ra dữ liệu
    cout << "NumFamous: " << numFamous << endl;
    cout << "Total money: " << fund << endl;
    for (int i = 0; i < numFamous; i++) {
        cout << "ID: " << ids[i] << ", price: " << price[i] << ", followers ";
        cout << "(" << followers[i].size() <<") :" ;
        for (int j = 0; j < followers[i].size(); j++) {
            cout << followers[i][j] << " ";
        }
        cout << endl;
    }
    file.close();
    }
    else {
        cout << "Unable to open file" << endl;
    }
}

struct Solution{
    Input input; 
    unordered_set<int> selected;     // những người nổi tiếng đã được chọn
    unordered_set<int> left;        // những người nổi tiếng chưa được chọn 
    //unordered_set<int> store;      
    
    // danh sách follower đã chọn
    int Used ;                    // tiền đã tiêu
    int score ;                  // số người đã được chọn 
    unordered_map<int,int> store;
    float ratioH = 0.39;
    vector<float> h1;
    vector<float> h2;

    void setLeft(){                           // thêm tất cả Famous vào danh sách chưa được chọn 
        //cout << " Loading setLeft ....." << endl;
        for(auto x : input.ids){
            left.insert(x);
        }
        //cout << " Done setLeft !" << endl;
    }
    void clearSolution(){     // setup lại lời giải về ban đầu
        //cout << " Loading clearSolution ...." << endl; 
        this->Used = 0;
        this->score = 0;
        this->left.clear();
        this->selected.clear();
        this->store.clear();
        setLeft();
       // cout << "Done clear solution !" << endl;
    } 
    void firstSolution(){  
        //cout << " Loading firstSolution ...." << endl;
        int pickID;
        clearSolution();                            // tạo lời giải ban đầu , id ngẫu nhiên
        while(Used <= input.fund){                 // chọn tới khi hết quỹ 
            pickID = rand()%input.numFamous +1;   // chọn id ngẫu nhiên 
            AddFamous(pickID);
        }
        if(Used > input.fund) pushFamous(pickID);
        //if(Used > input.fund) pushFamous(pickID);     //  
        //cout << " Done firstSolution !" << endl;
    }
    Solution(string filename){
        //cout << " Loading Constructor ..." << endl;
        this->input = Input(filename);  
        clearSolution();
        VecHeristic1();     // thiết lập vector heristic1 
        VecHeristic2();     // thiết lập vector heristic2
        //cout << "Done Constructor Solution !" <<endl;
    }
  

    void AddFamous(int id){                                     // thêm Famous vào danh sách chọn
        //cout << " Loading AddFamous ...." << endl;
        //if(Used + input.price[id] > input.fund) return;      // nếu sau khi thêm mà tràn quỹ , loại 
        //cout << "USed before add(" <<id<<"): " << Used <<endl;
        selected.insert(id);
        left.erase(id);
        Used += input.price[id-1];
        for(auto x : input.followers[id-1]){
            store[x]++;                            // thêm x phần tử vào store, tăng giá trị xuất hiện lên 1
        }
        score = store.size();
        //cout << "Used Added: " << Used << endl;
        //cout << " Done add famous!" << endl;
    }

    void pushFamous(int id){                              // bỏ chọn Famous 
        //cout << " Loading pushFamous ...." << endl;
        //cout << "ID before push(" <<id<<"): " <<endl;
        if(selected.count(id)>0){         // ktra xem có trong danh sách chọn chưa 
            selected.erase(id);
            left.insert(id);
            Used -= input.price[id-1];
            //cout << "Substract : " << input.price[id-1] << endl;
            for(auto x : input.followers[id-1]){
                store[x]--;
                if(store[x] == 0) store.erase(x);
            }
        }
        score = store.size();
        //cout << "Used Push: " << Used << endl;
        //cout << "done push famous !" << endl;
    }
    
    // tìm id của famous có phỏng đoán h1 tối ưu
    int GoodHeristic(unordered_set<int> u){
        //cout << " Loading GoodHeristic ...." << endl;
        float minRatio = 9999; 
        int minID = 0;

        for(auto id : u){
            float ratio  = input.price[id-1] / input.followers[id-1].size();   
            //cout << "id: " << id <<",ratio: "<< ratio << endl;
            if(ratio < minRatio){
                minRatio = ratio;
                minID = id;
            }
        }                 
        //cout << "Done GoodHeristic!" << endl;
        return minID;

    }

    // tạo lời giải ban đầu với heristic 1 : số follower / giá thuê lớn được coi là tốt
    void firstHeristic(){     
        //cout << " Loading firstHeristic ...." << endl;
        clearSolution();            
        unordered_set<int> newIds;                  // tạo danh sách id quy về heristic
        for(auto x:input.ids){
            newIds.insert(x);
        }
        int id;
        while(Used <= input.fund){       // bắt đầu chọn Famous với heristic giảm dần
            id = GoodHeristic(newIds);
            AddFamous(id);                  // thêm id famous vào danh sách chọn
            newIds.erase(id);              // xóa id vừa chọn khỏi danh sách id heristic
        }
        if(Used > input.fund) pushFamous(id);    
        //cout << " Done first Heristic !" << endl;
    }

    // NOTE : Heristic 2 : một follower theo dõi nhiều Famous. Famous chứa nhiều follower đó là tệ 

    // hàm trả về số idol của 1 follower
    int findRepeat(int idf){
        //cout << " Loading findRepeat ...." << endl;
        int count = 0;
        for(auto follow : input.followers){
            for(int f : follow){
                if(idf == f) count++;
            }
        }
        //cout << " Done find Repeat !" << endl;
        return count;
    }

    /* NOTE : Heristic 3 : Tính độ tệ của 1 Famous dựa trên tổng độ tệ của 1 follower
                           Độ tệ của 1 follower là 1 tỉ lệ (0->1) : số idol của người đó / tổng số idol( NumFamous)
                           Tỉ lệ này đại diện cho khả năng bị trùng lặp follower của 1 Famous với "tất cả" những Famous còn lại
    */
    // Hàm trả về % số idol của 1 follower / tổng số idol(numFamous) 
    float findPercent(int idf){
        return (float)findRepeat(idf)/input.numFamous;
    }

    // note1: 1 follower có trên 1 idol , khi tính tổng độ tệ của Famous, liệu có tính tổng số trùng lặp của từng follower , hay 
    // mỗi follower trùng lặp chỉ tính + 1 điểm tệ bất kể số idol theo dõi của follower đó

    // heristic 2.1 : tổng (số idol của 1 follower) của tất cả follower / tổng số follower . Tính trên 1 Famous
    // Heristic 2.2 : Tổng số follower bị trùng(có > 2 idol) / tổng số follwer

    // hàm trả về độ tệ của 1 vector - Heristic 2
    float repeatVector1(vector<int> u){
        float num = u.size();
        //cout << " Loading repeatVector ....." << endl;
        float numRepeat = 0;
        for(auto f : u){
            numRepeat += findRepeat(f);            //Heristic 2.1 : tổng số trùng lặp / số follower của 1 Famous
            //if(findRepeat(f) > 1) numRepeat++;     // Heristic 2.2 : số trùng lặp // số follower 
        }
        //cout << " Done repeatVector !" << endl;
        return numRepeat/num;
    }

    float repeatVector(vector<int> u){
        float num = u.size();
        //cout << " Loading repeatVector ....." << endl;
        float numRepeat = 0;
        for(auto f : u){
            numRepeat += findPercent(f);            
        }
        //cout << " Done repeatVector !" << endl;
        return numRepeat/num;
    }


    // hàm thiết lập vector chứa % về độ tốt đối với heristic1 của tất cả Famous  (từ 0 -> 1)
    void VecHeristic1(){
        //cout << " Loading VerHeristic1 ....." << endl;
        int max = -999999;
        int min = 999999;
        //vector<float> h1;            
        for(auto id : input.ids){
            //out << "id: "<< id;
            float ratio  = input.price[id-1] / input.followers[id-1].size();  
            //cout << ", Price(id "<<id<<"): " <<input.price[id-1] <<", Follow(id " <<id <<"): "<< input.followers[id-1].size() ; 
            if(ratio > max) max = ratio; 
            if(ratio < min)  min = ratio; 
            //cout << ", ratio of ID(" <<id <<"): " << ratio;
            h1.push_back(ratio);  
            //cout << " || ";                          
        }
        // chuẩn hóa 0->1 
        for(auto& h : h1){
            h -= min;
            h /= (max-min);            // tỉ lệ càng gần 0 càng tốt, càng gần 1 càng tệ 
            //h = 1-h;
            //cout <<"h1_scaled: " << h ;
            //cout << h << " " ;
        }
       // cout << " Done VecHeristic1 !" << endl;
        //return h1;
    }
    // NOTE : h1 và h2 phải đồng biến, nghĩa là càng gần 0 hoặc 1 thì càng tốt (tệ)

    // hàm thiết lập vector chứa % về độ tệ đối với heristic 2 của tất cả Famous ( từ 0 . 1)
    void VecHeristic2(){
        //cout << " Loading VecHeristic2 ......" << endl;
        float max = -1, min =1;
        //vector<float> h2;
        for(auto id : input.ids){
            //cout << "id: " <<id;
            float r = repeatVector(input.followers[id-1]);
            //cout << "r: " << r << " ";
            //r = 1/r;                        // nghịch biến h1, vì r càng lớn càng tệ. Phải đồng biến với h1
            if(r>max) max = r;
            if(r<min) min = r;
            h2.push_back(r);
            //cout << "r: " << r ;
        }
        // chuẩn hóa về dạng 0->1
        for(auto& h : h2){
            h -= min;
            h /= (max-min);
            //cout << "h: "<< h << " ";
            //cout <<"h_scaled: " << h <<" | ";
        }
        //cout << " Done VecHeristic2 !" << endl;
        //return h2;
    }

    // bây giờ tạo lời giải bằng cách kết hợp cả 2 heristic 
    // chọn độ ảnh hưởng của mỗi heristic :vd ratioH = 0.6 . Trọng số được tính h =  0.6*h1 + 0.4*h2

    // Kết hợp 2 Heristic
    // Hàm trả về vector chưa heristic tổng hợp của tất cả Famous 
    vector<float> VecHeristic(){
        //cout << " Loading VecHeristic ...." << endl;
        vector<float> H ;
        //vector<float> h1 = VecHeristic1();
        //vector<float> h2 = VecHeristic2();
        for(int i=0; i<input.numFamous;i++){
            float kq = ratioH*h1[i] + (1-ratioH)*h2[i];
            H.push_back(kq);
            //cout << "H["<<i<<"]"<<kq<<" ";
        }
        //cout << " Done VecHeristic !" << endl;
        return H;           // trọng số H càng lớn là càng tệ
    }

    int getMinIndex(unordered_map<int,float> a){
        //cout << "GetMaxIndes running ..." << endl;
        float min = 999;
        int id = 0;
        for(auto x : a){
            //cout << "x: " << x.second << " ";
            if(x.second <min){
                min = x.second;
                //cout <<"max update: " << max ;
                id = x.first;
            }
            //cout << endl;
        }
        return id;
    }

    // tạo lời giải ban đầu với heristic tổng hợp
    void MasterFirstSolution(){
        //cout << " Loading MasterFirstSolution ...." << endl;
        clearSolution();
        vector<float> H0 = VecHeristic();  
        unordered_map<int,float> H;
        for(int id = 0; id < H0.size() ;id++){
            H.insert(make_pair(id,H0[id]));
        }

        int minID;
        do{
            minID = getMinIndex(H);   // tìm id của Famous có heristic tổng hợp tốt nhất 
            AddFamous(minID+1);
            H.erase(minID);
        }while(Used <= input.fund);
        if(Used > input.fund) pushFamous(minID+1); 
        //cout << "Best score: " << score << endl;
        //cout << " Done MasterFirstSolution !" << endl;
    }

    // hàm trả về 1 unordered_set chứa pair<id,heristic> của 1 tập unordered_set khác(selected, left)
    unordered_map<int, float> makeUnorderHeristic(unordered_set<int> a){
        //cout << " Loading makeUnorderHeristic ....." << endl;
        unordered_map<int, float> Repeat ;      //
        vector<float> H = VecHeristic();
        for(auto id : a){
            float her = H[id-1];
            //cout <<"id: " << id <<",her: " <<H[id-1] <<" | ";
            Repeat[id]= her;
        }
        //cout << " Done MakeUnorderHeristic !" << endl;
        return Repeat;
        
    }
    queue<int> makeQueueSelect(){
        unordered_map<int, float> Her2Select = makeUnorderHeristic(selected);
        queue<int> queSelect;
        int minIDSelect;
        float max = -1;
        while(!Her2Select.empty()){
            for(auto f1 : Her2Select){
                if(f1.second >= max){
                    max = f1.second;
                    minIDSelect = f1.first;
                }
            }
            max = -1;
            queSelect.push(minIDSelect);
            Her2Select.erase(minIDSelect);
           
        }
        return queSelect;
    }
    queue<int> makeQueueLeft(){
        unordered_map<int,float> Her2Left = makeUnorderHeristic(left);
        queue<int> queLeft;
        int maxIDLeft;
        float min = 2;
        while(!Her2Left.empty()){
            for(auto f1 : Her2Left){
                if(f1.second <= min){
                    min = f1.second;
                    maxIDLeft = f1.first;
                }
            }
            min = 2;
            queLeft.push(maxIDLeft);
            Her2Left.erase(maxIDLeft);
           
        }
        return queLeft;
    }
    void localSearch(){
        cout << " Starting LocalSearch ..." << endl;
        int bestScore = this->score;
        int count = 0;
        queue<int> queSelect = makeQueueSelect();
        queue<int> queLeft = makeQueueLeft();
        //showq(queLeft);
        cout << "________" << endl;
        //showq(queSelect);
        queue<int> CoppyLeft = queLeft;
        showq(CoppyLeft);
        queue<int> CoppySelect = queSelect;

        do{
            int id1 = queSelect.front();
            //cout << "id1: " << id1 << endl;
            unordered_set<int> added;       // tập set lưu lại những id đã được thêm vào
            do{
                pushFamous(id1);
                //cout << "Used before add: " << Used << endl;
                while(Used <= input.fund){            // lấy Famous từ LEft cho tới khi đầy quỹ
                    if(queLeft.size() < 1) break;
                    count++;
                    int id2 = queLeft.front();
                    //cout <<"ID2: " << id2 << endl;
                    if(Used + input.price[id2-1]> input.fund){
                        break;  //dừng khi tràn quỹ
                    }else{
                        AddFamous(id2);
                        added.insert(id2);
                        //cout << "USed after add: " << Used << endl;
                        queLeft.pop();
                    }
                }
                //cout <<"Queue left size: " << queLeft.size() << endl;
                //cout << "added: " ;
                //for(auto id : added){
                    //cout << id << "-";
                //}
                //cout <<" So lan tach nhom: " << count-1 << endl;
                int newScore = this->score;
                //cout << "New Score: " << newScore << endl;
                if(newScore <= bestScore){
                    AddFamous(id1);
                    //cout << " Dont increase " << endl;
                    for(auto id : added){
                        pushFamous(id); 
                        //cout << "Push ID:" << id << endl;
                        //added.erase(id);
                        //cout << " added :" ;
                        for(auto k : added){
                            //cout << k <<"-";
                        }
                        //queLeft.pop();
                    }
                }else{
                    cout <<"New best Score : " << newScore << endl;
                    bestScore = newScore;
                    //queLeft.pop();
                }
                added.clear();
                if(queLeft.size() > 0) queLeft.pop();

            }while(!queLeft.empty());
            count = 0;
            queSelect.pop();
            id1 = queSelect.front();    // lấy ra id tiếp theo trong select;
            queLeft = CoppyLeft;            // khôi phục lại queLeft sau khi dùng hết
            //cout << "Select size: " << queSelect.size() << endl;
        }while(!queSelect.empty());
        
        cout << "Best score: " << bestScore << endl;
        cout << "USed: " << Used << endl;
        cout << "QUESELECT: " << endl;
        showq(queLeft);
        cout << "QUELEFT: " << endl; 
        showq(queSelect);
        
    }
    
    void showq(queue<int> gq){
        queue<int> g = gq;
        while (!g.empty()) {
            cout << '\t' << g.front();
            g.pop();
        }
        cout << '\n';
    }


    // hàm swap cho trường hợp 1:1
    void swap(){ 
        // cout << " Loading swap1 ....." << endl;
        // tạo danh sách độ tệ Hersistic của tập selected và tập left 
        unordered_map<int, float> Her2Select = makeUnorderHeristic(selected);
        unordered_map<int,float> Her2Left = makeUnorderHeristic(left);

        // bây giờ trao đổi 2 Famous giữa selected và left, nhưng không ngẫu nhiên hay lần lượt , mà theo heristic
        // quy tắc : ưu tiên swap giữa Famous có heristic tệ nhất bên selected và Famous có heristic tốt nhất bên left
        int minIDSelect, maxIDLeft;
        
        //cout << Used << endl;
        //return;
        int count = Her2Select.size();
        int count2 = Her2Left.size();
        //while(!Her2Select.empty()){
        while(count>0){
            count --;
            float max = -1;
            // lấy ra id có heristic tệ nhất trong selected
            for(auto f1 : Her2Select){  
                if(f1.second > max){
                    max = f1.second;
                    minIDSelect = f1.first;
                }
            }
            while(count2 > 0){
                count2--;
            //while(!Her2Left.empty()){
                //cout << " starting " << endl;
                //cout << "Used: " << Used << endl;
                float min = 1;
                // lấy ra id có herisic tốt nhất trong left 
                //cout << " HER2LEFT.SIZE()" << Her2Left.size() << endl;
                for(auto f2 : Her2Left){
                    if(f2.second < min){
                        cout << "F2.SECOND: " << f2.second<< " || " << f2.first << endl;
                        min = f2.second;
                        maxIDLeft = f2.first;
                    }
                }
                //cout << "MIN: " << min << endl;
                cout << "maxID: " << maxIDLeft << endl;
                if(Used + input.price[maxIDLeft] - input.price[minIDSelect] > input.fund){
                    //if(Her2Left.size() == 1) Her2Left.clear();
                    Her2Left.erase(maxIDLeft);
                    cout << "HEREEEEEE" << endl;
                    for(auto x : Her2Left){
                        cout << "IDLEFT: " << x.first << endl;
                    }
                    cout << "SIZE: "<< Her2Left.size() << endl;
                    //continue;

                }
                else{
                    while(Used + input.price[maxIDLeft] - input.price[minIDSelect] <= input.fund && count2 >0){  // chống tràn quỹ
                        // nhấc 1 Famous ra có thể thêm vài Famous khác vào
                        int oldScore = this->score;
                        AddFamous(maxIDLeft);
                        pushFamous(minIDSelect);
                        int newScore = this->score;
                        // nếu ko cải thiện, đi lại 
                        if(oldScore >= newScore){  
                            pushFamous(maxIDLeft);
                            AddFamous(minIDSelect);
                            cout << " ko cai thien " << endl;
                            count2--;
                            //break;
                        }
                        else {
                            cout <<"cai thien" << endl;
                            count2--;
                        }
                        Her2Left.erase(maxIDLeft);   // xóa id có heristic lớn nhất trong tập left
                        min = 1;
                        // lấy ra id có heristic lớn tiếp theo 
                        for(auto f2 : Her2Left){
                            if(f2.second < min){
                                min = f2.second;
                                maxIDLeft = f2.first;
                                //cout << "maxID update: " << maxIDLeft << " " << endl;
                            }
                        }
                    }
                }
                //if(Her2Left.size() == 1) break;
                cout << endl;
                Her2Left.erase(maxIDLeft);   // xóa id có heristic lớn nhất trong tập left
                    
            }  
            cout <<"here" << endl;
            // sau vòng while(), Her2Left đã rỗng, cần khôi phục lại
            Her2Left = makeUnorderHeristic(left);
            Her2Select.erase(minIDSelect); // xóa đi id có heristic nhỏ nhất trong selected 
        }
        cout << " Done Swap1 !" << endl;

    }
              
    void training(){
        cout << "Preparing to training.... " << endl;
        int bestScore = this->score;
        float bestRatioH = 0;
        bool direction = true;
        int count = 0;
        int count1 = 0;
        while(true){
            count1++;
            cout << "Epoch "<< count1 << " - ";
            int oldScore = this->score;
            //ratioH += 0.005;
            if(direction){
                ratioH += learning_rate;
            }
            else ratioH -= learning_rate;
            cout << "Ratio: " << ratioH << "-";
            MasterFirstSolution();
            int newScore = this->score;
            cout << " New score: " << newScore << endl;
            if(newScore >= bestScore){
                if(newScore > bestScore){
                    bestScore = newScore;
                    bestRatioH = ratioH;
                    cout << " New increase Score: " << bestScore << endl;
                    count = 0;
                }
            }
            // đổi hướng 
            else {   
                count ++;
                //direction = !direction;
            }
            // quay đầu
            if(ratioH < 0 || ratioH > 1) direction = !direction;
                //break;
            // dừng khi không cải thiẹn , chạy quá lâu
            if(count > 200) break;
        }
        cout << "Best Score :" << bestScore << endl;
        cout << "best ratioH: " << bestRatioH << endl;
        this->ratioH = bestRatioH;                           // lưu lại tỉ lệ tối ưu cho các lần training sau
        MasterFirstSolution();         // thực hiện lại Solution khi đã tìm được tỉ lệ tối ưu
        //cout << "Epoch: " << count1 << endl;
    }   

    void printSolution(){
        cout << " Loading PrintSolution !" << endl;
        cout << "So tien duoc cap: " << input.fund << endl;
        cout << "So tien thue la : " << Used << endl; 
        cout << " Co duoc : " << score << " Follower" ;
        cout << " Danh sach nhung nguoi duoc thue: " << endl;
        for(auto id : selected){
            cout << "ID: " << id << ", Price: " << input.price[id-1] ;
            cout << ", Follower" << "(" <<input.followers[id-1].size() << ") :" ;
            for(auto f : input.followers[id-1]){
                cout << f << " ";
            }
            cout << endl;
        }
        
    }

    // hàm trả về số trùng nhau giữa 1 tập follower(của 1 Famous) và selected
    int Interfer(vector<int> a){
        int count = 0;
        for(auto id : a){                   // ktra cho toàn bộ follower - độ phức tạp đạt min O(N)
            if(selected.find(id) == selected.end()) count++;
        }
        return count;
    }
    // Cập nhật :Khi thêm 1 Famous : xóa toàn bộ follower được thêm trong mỗi tập con của setRemaingFollower
    // return : remaining[id-1].size() : số follower sẽ được thêm mới của Famous(id);

    void setRemainingFollower(unordered_map<int,unordered_set<int>> a){   // ban đầu chưa có follower nào được chọn, tập remaining = tập input followers
        unordered_set<int> f;
        int count = 1;             // đồng bộ với id của Famous trong tập followers 
        for(auto follow : input.followers){  
            f.clear();
            for(auto id : follow){
                f.insert(id);
            }
            a[count] = f;
            count++;
        }
        cout << "remainingFollower: " << endl;
        for(auto f : a){
            cout << " ID: " << f.first ;
            for(auto id : f.second){
                cout << id <<" " ;
            }
            cout << endl;
        }
    }
    int getMaxRemainingID(unordered_map<int,unordered_set<int>> a){
        float max = -1;
        int countID = 1;    // đồng bộ với id
        int maxID;
        for(auto id : a){
            float r = (float)id.second.size()/input.price[countID-1];
            if(r > max){
                max = r;
                maxID = countID;
            }
        }
        
    }
    
    void puting(){
        //unordered_set<int> select;                    // các id đã được chọn 
        unordered_map<int,unordered_set<int>> RemainingFollower;
        setRemainingFollower(RemainingFollower);
        do{

        }while(Used < input.fund);
    }

};




int main(){
    srand(time(0));
    
    //Input p;      
    //string filename1 = "dataIM2.txt";
    //Tao1File("dataIM5.txt");
    //TaoNhieuFile();
    printData("dataIM1.txt");
    Solution s =  Solution("dataIM1.txt");
    //s.setLeft();
    s.firstSolution();
    //cout <<"FIRST SOLUTION !!" << endl;
    //s.printSolution();
    //s.firstHeristic();
    //cout <<"FIRST HERISTIC !!" << endl;
    s.MasterFirstSolution();
    s.training();
    s.localSearch();
    //s.training();
    //cout <<"MASTERHERISTIC !!" << endl;
    //s.localSearch();
    // unordered_map<unordered_set<int>> a;
    //s.setRemainngFollower(a);
    //p = Input("dataIM1.txt");
    //s.printSolution();
    //p.Display();
    //s.GoodHeristic(s.left);

}