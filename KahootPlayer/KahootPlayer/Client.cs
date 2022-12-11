using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace KahootPlayer
{
    public static class Client
    {
        static TcpClient client;
        static NetworkStream stream;

        public static void Connect(string ip, int port)
        {
            client = new TcpClient(ip, port);
            // Get a client stream for reading and writing.
            stream = client.GetStream();
        }
        public static void SetTimeout(int len)
        {
            client.ReceiveTimeout = len;
        }
        public static void Disconnect()
        {
            // Close everything.
            stream.Close();
            client.Close();
        }
        public static void Send(string msg)
        {
            try
            {
                Byte[] data = System.Text.Encoding.ASCII.GetBytes(msg);

                // Send the message to the connected TcpServer. 
                stream.Write(data, 0, data.Length);

                Console.WriteLine("Sent: {0}", msg);
            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine("ArgumentNullException: {0}", e);
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }
        }
        public static string Recv()
        {

            // Receive the TcpServer.response.

            // Buffer to store the response bytes.
            Byte[] data = new Byte[256];

            // String to store the response ASCII representation.
            String responseData = "error";

            try
            {
                // Read the first batch of the TcpServer response bytes.
                Int32 bytes = stream.Read(data, 0, data.Length);
                responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                Console.WriteLine("Received: {0}", responseData);
            }
            catch (ArgumentNullException e)
            {
                Console.WriteLine("ArgumentNullException: {0}", e);
            }
            catch (SocketException e)
            {
                Console.WriteLine("SocketException: {0}", e);
            }
            return responseData;
        }
    }
}