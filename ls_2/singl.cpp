// Declaration

class Singleton {
private:
    Singleton() = default;
    ~Singleton() = default;

    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;

    void* operator new(std::size_t) = delete;
    void* operator new[](std::size_t) = delete;

    void* operator delete(std::size_t) = delete;
    void* operator delete[](std::size_t) = delete;
public:
    static Singleton& getInst()
    {
        static Singleton object;
        return object;
    }

};

int main(int argc, char** argv)
{
    auto& s = Singleton::getInst();
}