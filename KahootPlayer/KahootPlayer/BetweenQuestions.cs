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
    [Activity(Label = "BetweenQuestions")]
    public class BetweenQuestions : Activity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            SetContentView(Resource.Layout.Between);
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
                catch{}
            }
            string[] msg = status.Split("#");
            status = msg[1];

            if (status == "CORRECT")
            {
                Intent intent = new Intent(this, typeof(Correct));
                intent.SetFlags(ActivityFlags.NewTask);
                StartActivity(intent);
                this.Finish();
            }
            else if (status == "WRONG")
            {
                Intent intent = new Intent(this, typeof(Wrong));
                intent.SetFlags(ActivityFlags.NewTask);
                StartActivity(intent);
                this.Finish();
            }
        }
    }
}