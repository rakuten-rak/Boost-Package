#include <boost/log/trivial.hpp>
#include <boost/asio.hpp> 
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators//statistics/stats.hpp>
#include <boost/accumulators//statistics/sum.hpp>
#include <boost/accumulators//statistics/count.hpp>
#include <boost/accumulators//statistics/max.hpp>
#include <boost/accumulators//statistics/mean.hpp>
#include <boost/accumulators//statistics/variance.hpp>

#include <iostream>

#include <string>
#include <unordered_map>

//using namespace boost::accumulators;

using Accumulator =
boost::accumulators::accumulator_set<
    double,
    boost::accumulators::stats <
    boost::accumulators::tag::count, boost::accumulators::tag::max,
    boost::accumulators::tag::mean,
    boost::accumulators::tag::variance,
    boost::accumulators::tag::sum
    >
>;

static std::unordered_map<std::string, Accumulator> stats;


void onRequest(const std::string &route, double t)
{   // start timer
    // === parsin the request
    // --> stop timer
    stats[route](t);
    // send the response

}


int main()
{
    BOOST_LOG_TRIVIAL(info) << "from boost";
    boost::asio::io_context ctx;

    for (size_t i = 0; i < 20;i++)
    {
        if (i == 0)
        {
            onRequest("indes", 20);
            onRequest("imprint", 10);

        }
        else
        {
            onRequest("indes", 5 + i / 3);
            if(i % 2 == 0)
                onRequest("imprint", 2 + i / 4);
        }
    }
    for (auto& acc : stats)
    {
        std::cout << acc.first << " : " <<
            boost::accumulators::count(acc.second) << " ~ " <<
            boost::accumulators::mean(acc.second) << " --> "
            << " =" << boost::accumulators::max(acc.second)
            << " #" << boost::accumulators::variance(acc.second) <<
             "==" << boost::accumulators::sum(acc.second) << std::endl;;

    }
}
