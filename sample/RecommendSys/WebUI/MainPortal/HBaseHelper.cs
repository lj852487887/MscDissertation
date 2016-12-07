using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Text;
using Thrift.Transport;
using Thrift.Protocol;

namespace MainPortal
{
    public class HBaseHelper
    {
        static TTransport transport = new TSocket("192.168.235.129", 9090);
        static TProtocol tProtocol = new TBinaryProtocol(transport);
        static Hbase.Client client = new Hbase.Client(tProtocol);

        public static void Open()
        {
            transport.Open();
        }

        public static void Close()
        {
            transport.Close();
        }

        /// <summary>  
        /// 通过rowkey获取数据  
        /// </summary>  
        /// <param name="tablename"></param>  
        /// <param name="rowkey"></param>  
        public static List<TRowResult> GetByRow(string tablename, string rowkey)
        {
            List<TRowResult> reslut = client.getRow(Encoding.UTF8.GetBytes(tablename), Encoding.UTF8.GetBytes(rowkey), null);
            return reslut;
        }

        /// <summary>  
        /// 通过Rowkey前缀Fliter  
        /// </summary>  
        /// <param name="tablename"></param>  
        /// <param name="startrowkey"></param>  
        /// <param name="endrowkey"></param>  
        public static List<TRowResult> GetByRowFilter(string tablename, string Prefixrowkey, List<string> _cols)
        {
            List<byte[]> _bytes = new List<byte[]>();
            foreach (string str in _cols)
                _bytes.Add(Encoding.UTF8.GetBytes(str));


            int ScannerID = client.scannerOpenWithPrefix(Encoding.UTF8.GetBytes(tablename), Encoding.UTF8.GetBytes(Prefixrowkey),
                _bytes, null);
            /* 
            *  scannerGetList(string ID),源码中其实调用scannerGetList(string ID,int nbRow)方法，nbRow传值为1 
            */
            List<TRowResult> reslut = client.scannerGetList(ScannerID, 100);
            return reslut;
        }

        /// <summary>  
        /// 通过RowKey的范围获取数据  
        /// </summary>  
        /// <param name="tablename"></param>  
        /// <param name="stRowkey"></param>  
        /// <param name="?"></param>  
        /// <remarks>结果集包含StartRowKey列值，不包含EndRowKey的列值</remarks>  
        public static List<TRowResult> GetByRowStartEnd(string tablename,
            string stRowkey, string endRowkey, List<string> _cols)
        {
            List<byte[]> _bytes = new List<byte[]>();
            foreach (string str in _cols)
                _bytes.Add(Encoding.UTF8.GetBytes(str));


            int ScannerID = client.scannerOpenWithStop(Encoding.UTF8.GetBytes(tablename),
                Encoding.UTF8.GetBytes(stRowkey), Encoding.UTF8.GetBytes(endRowkey),
                _bytes, null);

            List<TRowResult> reslut = client.scannerGetList(ScannerID, 100);
            return reslut;
        }

        /// <summary>  
        /// 通过Filter进行数据的Scanner  
        /// </summary>  
        /// <param name="tablename"></param>  
        /// <param name="filterString"></param>  
        public static List<TRowResult> GetByFilter(string tablename, string filterString, List<byte[]> _cols, int num)
        {
            TScan _scan = new TScan();
            //SingleColumnValueFilter('i', 'Data', =, '2')  
            _scan.FilterString = Encoding.UTF8.GetBytes(filterString);
            _scan.Columns = _cols;

            int ScannerID = client.scannerOpenWithScan(Encoding.UTF8.GetBytes(tablename), _scan, null);

            List<TRowResult> reslut = client.scannerGetList(ScannerID, num);
            return reslut;
        }

        public static bool UpdateRow(string tablename, string rowkey, List<Mutation> _mutations)
        {
            try
            {
                client.mutateRow(Encoding.UTF8.GetBytes(tablename), Encoding.UTF8.GetBytes(rowkey), _mutations, null);
                return true;
            }
            catch (Exception e)
            {
                return false;
            }
        }

        public static bool UpdateRows(string tablename, List<BatchMutation> _BatchMutation)
        {
            try
            {
                client.mutateRows(Encoding.UTF8.GetBytes(tablename), _BatchMutation, null);
                return true;
            }
            catch (Exception e)
            {

                return false;
            }

        }

        public static bool DeleteRow(string tablename, string rowkey, string column)
        {
            try
            {
                client.deleteAll(Encoding.UTF8.GetBytes(tablename), Encoding.UTF8.GetBytes(rowkey),
                    Encoding.UTF8.GetBytes(column), null);
                return true;
            }
            catch (Exception e)
            {

                return false;
            }

        }

        public static bool DeleteRows(string tablename, string rowkey)
        {
            try
            {
                client.deleteAllRow(Encoding.UTF8.GetBytes(tablename), Encoding.UTF8.GetBytes(rowkey), null);
                return true;
            }
            catch (Exception e)
            {
                return false;
            }

        }

        public static bool DeleteTable(string tablename)
        {
            try
            {
                client.deleteTable(Encoding.UTF8.GetBytes(tablename));
                return true;
            }
            catch (Exception e)
            {
                return false;
            }

        }

        public static bool CreateTable(string tablename, List<ColumnDescriptor> _cols)
        {
            try
            {
                client.createTable(Encoding.UTF8.GetBytes(tablename), _cols);
                return true;
            }
            catch (Exception e)
            {
                return false;
            }

        }
    }
}