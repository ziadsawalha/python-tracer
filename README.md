Python Tracing Tool
===================

This is a tool used to enable tracing dynamically and provide a call graph in real-time for a python model. I created it because debugging was way
too painful for me.

Instructions are in the tools/tracer.py file.

Example is in example.py (with instructions in the comment).

The output of the tracer includes:

 * functions called (relative path)
 * calling function
 * exceptions in red

It does not include system calls.

I tested this on a Mac. If it doesn't work on WIndows or Linux, please post a fix :-)


I hope you find this as useful as I did!