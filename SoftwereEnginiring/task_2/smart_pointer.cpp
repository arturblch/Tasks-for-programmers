#include <stdio.h>

class Person
{
    int age;
    char* pName;

    public:
        Person(): pName(0),age(0){}
        Person(char* pName, int age): pName(pName), age(age){}
        ~Person(){}
        void Display()
        {
            printf("Name = %s Age = %d \n", pName, age);
        }
};

class Counter
{
    private:
    int count; // Reference count

    public:
    void AddRef()
    {
        // Increment the reference count
        count++;
    }

    int Release()
    {
        // Decrement the reference count and
        // return the reference count.
        return --count;
    }

    int GetCount()
    {
        return count;
    }
};


template < typename T > 
class SmartPointer
{
private:
    T*    pData;       // pointer
    Counter* reference; // Reference count

public:
    SmartPointer() : pData(0), reference(0) 
    {
        // Create a new reference 
        reference = new Counter();
        // Increment the reference count
        reference->AddRef();
    }

    SmartPointer(T* pValue) : pData(pValue), reference(0)
    {
        // Create a new reference 
        reference = new Counter();
        // Increment the reference count
        reference->AddRef();
    }

    SmartPointer(const SmartPointer<T>& sp) : pData(sp.pData), reference(sp.reference)
    {
        // Copy constructor
        // Copy the data and reference pointer
        // and increment the reference count
        reference->AddRef();
    }

    ~SmartPointer()
    {
        // Destructor
        // Decrement the reference count
        // if reference become zero delete the data
        printf("counter = %d\ndelete\n", reference->GetCount());
        if(reference->Release() == 0)
        {
            printf("delete data and counter");
            delete pData;
            delete reference;
        }
    }

    T& operator* ()
    {
        return *pData;
    }

    T* operator-> ()
    {
        return pData;
    }
    
    SmartPointer<T>& operator = (const SmartPointer<T>& sp)
    {
        if (this != &sp) // Avoid self assignment
        {
            // Decrement the old reference count
            // if reference become zero delete the old data
            if(reference->Release() == 0)
            {
                delete pData;
                delete reference;
            }

            // Copy the data and reference pointer
            // and increment the reference count
            pData = sp.pData;
            reference = sp.reference;
            reference->AddRef();
        }
        return *this;
    }
};

int main()
{
    SmartPointer<Person> p(new Person("Scott", 25));
    p->Display();
    {
        SmartPointer<Person> q;
        SmartPointer<Person> r;
        q = r = p;
        r->Display();
        q->Display();

        // Destructor of q will be called here..
        // Destructor of r will be called here..
    }
    p->Display();
    // Destructor of p will be called here 
    // and person pointer will be deleted
}