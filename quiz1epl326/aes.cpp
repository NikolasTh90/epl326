#include <iostream>
#include <omp.h>
#include <chrono>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <stdbool.h>
#include <fstream>
#include <unistd.h>
using namespace std;
vector<string> words;


vector<int> copy(vector<int> list1) {
    vector<int> new_list;
    for (int i = 0; i < list1.size(); i++) {
        new_list.push_back(list1[i]);
    }
    return new_list;
}

vector<vector<int>> generateKeys(vector<vector<int>> keys, string alphabet) {
    vector<vector<int>> new_keys;
    if (keys.size() == 0) {
        for (int letter = 0; letter < alphabet.size(); letter++) {
            vector<int> temp;
            temp.push_back(letter);
            new_keys.push_back(temp);
        }
        return new_keys;
    }

    for (int i = 0; i < keys.size(); i++) {
        for (int letter = 0; letter < alphabet.size(); letter++) {
            vector<int> temp = copy(keys[i]);
            temp.push_back(letter);
            new_keys.push_back(temp);
        }
    }
    return new_keys;
}

string decrypt_openssl(std::vector<std::string>& parameters) {
    
    try {
        std::string decrypted_data = "";
        for (auto& s : parameters) {
            decrypted_data += s + " ";
        }
        decrypted_data.pop_back();
        // 2 is stderror code so throw it in a file
        std::string cmd = "openssl " + decrypted_data + " 2> /dev/null";
        char buffer[128];
        string possible_plaintext = "";
        // open a pipe for terminal
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe) {
            std::cerr << "Error: failed to open pipe\n";
            return "";
        }
        while (!feof(pipe)) {
            if (fgets(buffer, 128, pipe) != nullptr) {
                std::string data(buffer);
                if (data.size() > 0 && data[data.size() - 1] == '\n') {
                    data.pop_back();
                }
                if (data.size() > 0 && data[data.size() - 1] == '\r') {
                    data.pop_back();
                }
                possible_plaintext += data;
            }
        }
        int detected_words = 0;
        string word = "";
        int status = pclose(pipe);
        // status 0 means no error
        if (status == 0) {         
            for (int i=0; i<=possible_plaintext.length(); i++) {
                if (possible_plaintext[i]==' ') {
                    for (int j=0;j<words.size();j++){
                        if (word==words.at(j)) {
                        detected_words+=1;
                        break;
                        }
                    }
                    word="";
                }
                else {
                    word+=possible_plaintext[i];
                }
            }

            if (detected_words>1) {
                cout<<endl;
                for (int k=0; k<parameters.at(5).size(); k++) {
                    cout<<parameters.at(5).at(k);
                }
                cout<<endl;
                cout<<possible_plaintext<<endl;
            }   
    // return stringdecrypted + " num_words " + to_string(detected_words);

            return possible_plaintext;
        }
    } catch (const std::exception& e) {
        // std::cerr << "Error: " << e.what() << std::endl;
    }
    return "";
}



void run_AES_integer_key(string ciphertext_file){
    auto start_time = chrono::high_resolution_clock::now();

    // Vector that contains all vigenere(size) keys 
    // Each vector<vector> vigenere(size) contains all keys for this size
    // Each vector<vector<vector<int>>> vigenere(size) contains all keys and for each key all integer keys 
    vector<vector<vector<int>>> keys;
    int max_key_size = 6;
    for (int key_size=0; key_size<max_key_size; key_size++){       
        // Generate all vigenere(0) keys
        if (key_size == 0){
            keys.push_back(generateKeys({},"0123456789"));
        }
        // Generate all vigenere(key_size) keys by giving to function the 
        // previous vigenere(key-size-1) and generate all vigenere(key_size) keys
        // Add all vigenere(key_size) keys to keys vector
        else{
            keys.push_back(generateKeys(keys[key_size-1], "0123456789"));
        }
        cout << keys.at(key_size).size() << endl;
    }
    vector<string> keys_to_try;
    cout << "Start ";
    # pragma omp parallel
    {
        // cout<<omp_get_num_threads()<<endl;
        // cout<<keys.at(5).size()<<endl;

        //Keep only keys starting from 9
        #pragma omp single 
        {
            for (int i=0; i < keys.at(5).size(); i++){
                string key = "";
                    if (keys.at(5).at(i).at(0)==9){
                        for(int keyIndex=0;keyIndex<keys.at(5).at(i).size();keyIndex++){
                            key+=to_string(keys.at(5).at(i).at(keyIndex));
                        }
                        keys_to_try.push_back(key);
                    }
            }
   
        }
        # pragma omp for
        // Try all keys loop remove the single
        // for (int i=0; i < keys.at(5).size(); i++){
        //     string key = "";    
        //         for(int keyIndex=0;keyIndex<keys.at(5).at(i).size();keyIndex++){
        //             key+=to_string(keys.at(5).at(i).at(keyIndex));
        //         }
        //         //cout<<key<<endl;
        //         vector<string> parameters;
        //         string decrypted;
        //         // parameters = {"aes-128-ecb", "-d", "-in", ciphertext_file, "-k", key};
        //         // decrypted = decrypt_openssl(parameters);  
        //         parameters = {"aes-128-cbc", "-d", "-in", ciphertext_file, "-k", key};
        //         decrypted = decrypt_openssl(parameters);
        //     }
        for (int i=0; i < keys_to_try.size(); i++){
            string key = "";    
            key = keys_to_try.at(i);
            //cout<<key<<endl;
            vector<string> parameters;
            string decrypted;
            // parameters = {"aes-128-ecb", "-d", "-in", ciphertext_file, "-k", key};
            // decrypted = decrypt_openssl(parameters);  
            parameters = {"aes-128-cbc", "-d", "-in", ciphertext_file, "-k", key};
            decrypted = decrypt_openssl(parameters);
        }


    }
    cout << "End" << endl;
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time);
    cout << "Execution time: " << duration.count()/(1000000.0 * 60)  << " minutes." << endl << endl;
}

vector<string> dictionary() {
    ifstream dictionary("dictionary.txt");
    vector<string> list_of_words;
    string word;
    while (getline(dictionary, word)) {
        list_of_words.push_back(word);
    }
    dictionary.close();
    return list_of_words;
}

int main(int argc, char* argv[]){
    if (argc == 2){
        omp_set_num_threads(stoi(argv[1]));
    }
    auto start_time = chrono::high_resolution_clock::now();
    words=dictionary();   
    run_AES_integer_key("puzzle5");
    auto end_time = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time);
    cout << "Execution time: " << duration.count()/(1000000.0 * 60)  << " minutes." << endl;
}