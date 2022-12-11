using Android.App;
using Android.OS;
using Android.Support.V7.App;
using Android.Runtime;
using Android.Widget;
using Android.Views;
using Android.Content;

namespace KahootPlayer
{
    
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]

    public class MainActivity : AppCompatActivity
    {
        Button btnLogin, btnReg;
        EditText etUname, etPword;
        string IP = "172.20.10.6";
        int PORT = 5000;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);
            //Connect to server
            Client.Connect(IP, PORT);

            etUname = FindViewById<EditText>(Resource.Id.etUname);
            etPword = FindViewById<EditText>(Resource.Id.etPword);
            btnLogin = FindViewById<Button>(Resource.Id.btnLogin);
            btnReg = FindViewById<Button>(Resource.Id.btnReg);
           

            btnLogin.Click += BtnLogin_Click;
            btnReg.Click += BtnReg_Click;
        }

        private void BtnReg_Click(object sender, System.EventArgs e)
        {
            Intent intent = new Intent(this, typeof(Register));

            StartActivity(intent);
        }

        private void BtnLogin_Click(object sender, System.EventArgs e)
        {
            if (etUname.Text.Length > 0 && etPword.Text.Length > 0)
            {
                string data = "#LOG#" + etUname.Text + "#" + etPword.Text;
                string lendata = data.Length.ToString().PadLeft(5, '0') + data;
                Client.Send(lendata);
                
                string status = Client.Recv();
                string[] msg = status.Split("#");
                status = msg[1];
                if (status == "IN")
                {
                    Intent intent = new Intent(this, typeof(PIN));
                    intent.PutExtra("UName", etUname.Text);
                    intent.SetFlags(ActivityFlags.NewTask);
                    StartActivity(intent);
                    this.Finish();
                }
                else if (status == "WRNG")
                {
                    Toast.MakeText(this, "Wrong password or username given!\n Please enter correct logging details", ToastLength.Long).Show();
                    etUname.Text = "";
                    etPword.Text = "";
                }

            }
        }

        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }

    }
}