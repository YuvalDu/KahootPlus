using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace KahootPlayer
{
    [Activity(Label = "Waiting")]
    public class Waiting : Activity
    {
        String GameIP, UName;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Waiting);
            // Create your application here

            GameIP = Intent.GetStringExtra("GameIP") ?? "not available";
            UName = Intent.GetStringExtra("UName") ?? "not available";

            //Client.Connect(GameIP, 8000);
            Client.Connect("172.20.10.6", 8000);

            string data = "#NEW#" + UName;
            string lendata = data.Length.ToString().PadLeft(5, '0') + data;
            Client.Send(lendata);

            Thread t = new Thread(AsyncRecv);
            t.Start();
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

            if (status == "GO")
            {
                Intent intent = new Intent(this, typeof(Answer));
                intent.SetFlags(ActivityFlags.NewTask);
                StartActivity(intent);
                this.Finish();
            }
        }
    }
}