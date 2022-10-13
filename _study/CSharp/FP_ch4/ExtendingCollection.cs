using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ExtendingInterface;

namespace ExtendingInterface
{
    public static class IDataSourceExtension
    {
        public static IEnumerable<DataItem> GetItemsByGender(
            this IDataSource src,
            string gender)
        {
            foreach (DataItem item in src.GetItems())
            {
                if (item.Gender == gender)
                    yield return item;
            }
        }
    }
}
namespace FP_ch4
{
    public static partial class IDataSourceCollectionExtension
    {
        public static IEnumerable<DataItem> GetAllItemsByGender_IEnum(
            this IEnumerable src, string gender)
        {
            var items = new List<DataItem>();
            foreach (var s in src)
            {
                var refDataSource = s as IDataSource;
                if (refDataSource != null)
                {
                    items.AddRange(refDataSource.GetItemsByGender(gender));
                }
            }
            return items;
        }
    }
}
