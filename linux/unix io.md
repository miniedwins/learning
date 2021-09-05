# UNIX I/O



# I/O Type



## Buffered I/O



## Direct I/O



Direct I/O bypasses the file system buffer cache and **is able to perform asynchronous, overlapped I/Os.** The following benefits are provided:

- Faster response time. A user waits less time for Essbase to return data.
- Scalability and predictability. Essbase lets you customize the optimal cache sizes for its databases.



### Benefits of direct I/O  

***IBM Artice***

The primary benefit of direct I/O is to reduce CPU utilization for file reads and writes by eliminating the copy from the cache to the user buffer.

This can also be a benefit for file data which has a very poor cache hit rate. If the cache hit rate is low, then most read requests have to go to the disk. Direct I/O can also benefit applications that must use synchronous writes because these writes have to go to disk. In both of these cases, CPU usage is reduced because the data copy is eliminated.

A second benefit of direct I/O is that it allows applications to avoid diluting the effectiveness of caching of other files. Anytime a file is read or written, that file competes for space in the cache. This situation may cause other file data to be pushed out of the cache. If the newly cached data has very poor reuse characteristics, the effectiveness of the cache can be reduced. Direct I/O gives applications the ability to identify files where the normal caching policies are ineffective, thus releasing more cache space for files where the policies are effective.

**Performance costs of direct I/O**

Although direct I/O can reduce CPU usage, using it typically results in the process taking longer to complete, especially for relatively small requests. This penalty is caused by the fundamental differences between normal cached I/O and direct I/O.

**Direct I/O reads**

Every direct I/O read causes a synchronous read from disk; unlike the normal cached I/O policy where read may be satisfied from the cache. This can result in very poor performance if the data was likely to be in memory under the normal caching policy.

Direct I/O also bypasses the normal JFS or JFS2 read-ahead algorithms. These algorithms can be extremely effective for sequential access to files by issuing larger and larger read requests and by overlapping reads of future blocks with application processing.

Applications can compensate for the loss of JFS or JFS2 read-ahead by issuing larger read requests. At a minimum, direct I/O readers should issue read requests of at least 128k to match the JFS or JFS2 read-ahead characteristics.

Applications can also simulate JFS or JFS2 read-ahead by issuing asynchronous direct I/O read-ahead either by use of multiple threads or by using the **aio_read** subroutine.

**Direct I/O writes**

Every direct I/O write causes a synchronous write to disk; unlike the normal cached I/O policy where the data is merely copied and then written to disk later. This fundamental difference can cause a significant performance penalty for applications that are converted to use direct I/O.



## Synchronous I/O

***IBM Artice***

### Asynchronous disk I/O performance tuning

If an application does a synchronous I/O operation, it must wait for the I/O to complete. In contrast, asynchronous I/O operations run in the background and do not block user applications. This improves performance, because I/O operations and applications processing can run simultaneously. Many applications, such as databases and file servers, take advantage of the ability to overlap processing and I/O.

Applications can use the **aio_read()**, **aio_write()**, or **lio_listio()** subroutines (or their 64-bit counterparts) to perform asynchronous disk I/O. Control returns to the application from the subroutine as soon as the request has been queued. The application can then continue processing while the disk operation is being performed.

To manage asynchronous I/O, each asynchronous I/O request has a corresponding control block in the application's address space. This control block contains the control and status information for the request. It can be used again when the I/O operation is completed.

The user application can determine how to be notified when the I/O operation completes in the following ways:

- The application can poll the status of the I/O operation.
- The system can asynchronously notify the application when the I/O operation is done.
- The application can block until the I/O operation is complete.

Each I/O is handled by a single kernel process, or kproc, and typically the kproc cannot process any more requests from the queue until that I/O has completed. The default value of the `minservers` tunable is 3, and that of the `maxservers` tunable is 30. The `maxservers` value is the number of async I/O kprocs per processor. To obtain the maximum number of asynchronous I/O kprocs running on an AIX® system, multiply the `maxservers` value with the number of currently running processors.

All of the AIO tunables have a current, default, minimum and maximum value that can be viewed with the [**ioo**](https://www.ibm.com/docs/en/ssw_aix_72/i_commands/ioo.html) command. Only the current value can be changed with the **ioo** command. The other three values are fixed and are presented to inform the user of the bounds of the tunable. The current value of the tunable can be changed at any time and can be made persistent across operating system restarts. In systems that seldom run applications that use asynchronous I/O, the defaults are usually adequate.

It is important to note that both `minservers` and `maxservers` are per-processor tunables. Both of these tunables are dynamic, but changes to their values do not result in a synchronous change in the number of available servers in the system. If the value of `minservers` is increased, the actual number of servers rises directly proportional to the number of concurrent I/O requests. Once the new `minservers` value is reached, it becomes the new floor. Conversely, when `minservers` is decreased, the number of available servers naturally falls to that level as servers exit due to inactivity. If the number of async I/O requests is high, increase the `maxservers` value to approximately the number of simultaneous I/Os there might be. It is usually better to leave the `minservers` parameter at the default value because the AIO kernel extension will generate additional servers if needed.

# I/O Mode

