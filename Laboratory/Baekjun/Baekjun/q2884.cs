using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Baekjun
{
    class q2884
    {
        static void Main(string[] args)
        {
            //string[] input = Console.ReadLine().Split();
            //int inputTime = int.Parse(input[0]) * 60 + int.Parse(input[1]);

            //int convertedTime = inputTime - 45;

            //if (convertedTime > 0)
            //{
            //    int outputHr = convertedTime / 60;
            //    int outputMin = convertedTime % 60;

            //    Console.WriteLine("{0} {1}", outputHr, outputMin);
            //}
            //else if (convertedTime < 0)
            //{
            //    int outputHr = (1440 + convertedTime) / 60;
            //    int outputMin = (1440 + convertedTime) % 60;

            //    Console.WriteLine("{0} {1}", outputHr, outputMin);
            //}


            string[] time = Console.ReadLine().Split();

            // 시간 값을 h에 저장
            int h = int.Parse(time[0]);
            // 분 값을 m에 저장
            int m = int.Parse(time[1]);

            // m에서 45를 뺀다.
            m -= 45;

            // m이 음수인지 판단
            if (m < 0)
            {
                // m이 음수였다면 m에 60을 더해주고 h에서 1을 빼준다.
                m += 60;
                h -= 1;

                // h가 음수인지 확인하고 음수라면 23으로 바꿔준다.
                if (h < 0) h = 23;
            }
            // 계산된 값을 출력해준다.
            Console.WriteLine($"{h} {m}");
        }
    }
}
