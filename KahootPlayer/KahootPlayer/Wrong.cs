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
using System.Text;
using System.Threading;

namespace KahootPlayer
{
    [Activity(Label = "Wrong")]
    public class Wrong : Activity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Wrong);
            // Create your application here
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
            else if (status == "FIN")
            {
                Intent intent = new Intent(this, typeof(Done));
                intent.PutExtra("UName", msg[2]);
                intent.PutExtra("Points", msg[3]);
                intent.SetFlags(ActivityFlags.NewTask);
                StartActivity(intent);
                this.Finish();
            }
        }

    }
}