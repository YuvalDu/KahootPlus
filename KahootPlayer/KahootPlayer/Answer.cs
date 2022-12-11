using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace KahootPlayer
{
    [Activity(Label = "Answer")]
    public class Answer : Activity
    {
        Button btnGreen0, btnRed1, btnYellow2, btnBlue3;
        Thread t;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Answer);
            // Create your application here
            btnGreen0 = FindViewById<Button>(Resource.Id.btnGreen0);
            btnRed1 = FindViewById<Button>(Resource.Id.btnRed1);
            btnYellow2 = FindViewById<Button>(Resource.Id.btnYellow2);
            btnBlue3 = FindViewById<Button>(Resource.Id.btnBlue3);

            btnGreen0.Click += BtnGreen0_Click;
            btnRed1.Click += BtnRed1_Click;
            btnYellow2.Click += BtnYellow2_Click;
            btnBlue3.Click += BtnBlue3_Click;

            t = new Thread(AsyncRecv);
            t.Start();
            
        }
        private void BtnGreen0_Click(object sender, EventArgs e)
        {
            SendAnswer("0");
        }
        private void BtnRed1_Click(object sender, EventArgs e)
        {
            SendAnswer("1");
        }
        private void BtnYellow2_Click(object sender, EventArgs e)
        {
            SendAnswer("2");
        }
        private void BtnBlue3_Click(object sender, EventArgs e)
        {
            SendAnswer("3");
        }
        private void SendAnswer(string an)
        {
            t.Abort();
            string data = "#AN#" + an;
            string lendata = data.Length.ToString().PadLeft(5, '0') + data;
            Client.Send(lendata);
            Intent intent = new Intent(this, typeof(BetweenQuestions));
            intent.SetFlags(ActivityFlags.NewTask);
            StartActivity(intent);
            this.Finish();

        }
        private void AsyncRecv()
        {
            bool start = false;
            string status = "";
            Client.SetTimeout(1);
            while (!start)
            {
                try
                {
                    status = Client.Recv();
                    start = true;
                }
                catch { }

            }
            string[] msg = status.Split("#");
            status = msg[1];

            if (status == "WRONG")
            {
                Intent intent = new Intent(this, typeof(Wrong));
                intent.SetFlags(ActivityFlags.NewTask);
                StartActivity(intent);
                this.Finish();
            }
        }

    }
    
}