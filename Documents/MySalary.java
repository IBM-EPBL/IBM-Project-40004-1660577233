public class MySalary {
    public static void main(String[] args)  {
    int salaries[];
    int index=0;
    salaries=new int[4];
    while(index<4)  {
        salaries[index]=10000;
        index++;
    }
    System.out.println(salaries[3]);
}
}