#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

#define thread_tab_var_size 10
#define sleep_max 10
int threads;

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
 

void shleep(int index){
    int shleepy = rand() % sleep_max+1;
    printf("\n[THREAD] %d: Usypianie na %d sekundy.\n", index, shleepy);
    sleep(shleepy);
    printf("\n[THREAD] %d: Zakonczony.\n", index);
}
// bubble sort
void sorting(int index)
{
    //wygenerowanie danych do sortowania
    int temp_tab[thread_tab_var_size];

    for(int i =0 ;i<thread_tab_var_size;i++)
    {
            temp_tab[i] = rand() % 101;
    }

    //bubble sort
    for(int j = 0; j<thread_tab_var_size - 1; j++)
        for(int i = 0; i<thread_tab_var_size - j - 1; i++)
        {
            if (temp_tab[i] > temp_tab[i+1]) swap(&temp_tab[i],&temp_tab[i+1]);
        }
        //wypisanie wyniku
    printf("[THREAD] %d:",index);
    for(int i =0 ;i<thread_tab_var_size;i++)
        {
            printf("[%d]: %d",i,temp_tab[i]);
        }
}

//bubble sort, aleS dane sa bliskie do nieoptymalnych
void sorting_but_worse(int index)
{
    int temp_tab[thread_tab_var_size];
    for(int i =0 ;i<thread_tab_var_size;i++)
    {
        if(!i)    temp_tab[i] = rand() % 101;
        else{
            temp_tab[i] = rand() % 101;
            if(temp_tab[i-1]>=temp_tab[i]) temp_tab[i] += rand() % 101;
        }    

    }
        //bubble sort
    for(int j = 0; j<thread_tab_var_size - 1; j++)
        for(int i = 0; i<thread_tab_var_size - j - 1; i++)
        {
            if (temp_tab[i] < temp_tab[i+1]) swap(&temp_tab[i],&temp_tab[i+1]);
        }
        //wypisanie wyniku
    printf("[THREAD] %d:",index);
    for(int i =0 ;i<thread_tab_var_size;i++)
        {
            printf("[%d]: %d",i,temp_tab[i]);
        }


}

void caesar_salad(int index)
{
    char salad [thread_tab_var_size];
    for(int i = 0;i<thread_tab_var_size;i++) 
    {
        salad[i] = 65 + rand()%27;
    }
    int caesar = rand()%28; 
    printf("[THREAD] %d: poczatkowe slowo: %s \n",index,salad);
    for(int i = 0;i<thread_tab_var_size;i++)
    {
        if (salad[i]== ' ') break;
        salad[i] =salad[i] + caesar;
    }
    printf("[THREAD] %d: Slowo zostalo zmienione na: %s",index,salad);
}

void rando(int index)
{
    int lucky = rand()%100000001;
    int try = -1;
    while (lucky != try) try = rand()%100000001;
    printf("[THREAD] %d: Mamy zwyciesce! %d",index,try);
}

void *function(void *arguments)
{
    int func_amount = 4;
    int index = *((int*) arguments);
    switch(index%func_amount)
    {
        case 0:
            printf("[THREAD] %d: Watek rozpoczyna sortowanie losowych wartosci\n", index);
            sorting(index);
            break;
        case 1:
            printf("[THREAD] %d: Watek rozpoczyna sortowanie losowych wartosci o nieoptymalnym rozlozeniu\n", index);
            sorting_but_worse(index);
            break;
        case 2:
            printf("[THREAD] %d: Watek przenosi o losowa wartosc (wedlug tablicy ascii) wszystkie znaki z podanego przez uzytkonwika slowa: \n", index);
            caesar_salad(index);
            break;
        case 3:
            printf("[THREAD] %d: Watek losuje dwie liczby w zakresie 0 - 10M az trafi na dwie takie same liczby\n", index);
            rando(index);
            break;
        default:
            printf("[THREAD] %d: Watek nie dostal funkcji. Watek zostanie uspiony.\n", index);
            break;
    }

    shleep(index);
    return NULL;
}


int main(void)
{
    srand(time(NULL));
    // temporary definition of the tab of threads
    printf("[MAIN] Podaj ilosc porzadanych watkow: ");
    scanf("%d", &threads);
    //threads = 5;
    int* thread_tab;
    pthread_t *main_tab;

    main_tab = (pthread_t*) calloc(threads, sizeof(pthread_t));
    thread_tab = (int*) calloc(threads, sizeof(int));

    for(int i = 0; i<threads;i++)
    {
        printf("[MAIN]: Tworzenie watku %d.\n", i);
        thread_tab[i] = i;
        pthread_create(&main_tab[i],NULL,function, &thread_tab[i]);
    }

    printf("[MAIN]: Wszystkie watki zostaly stworzone.\n");

    for (int i = 0; i < threads; i++) 
    {
        pthread_join(main_tab[i], NULL);
        printf("[MAIN]: Watek %d zakonczony.\n", i);
    }
    free(main_tab);
    free(thread_tab);
    printf("END");
    return 0;
}