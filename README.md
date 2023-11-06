# LibreOfficeHistorian
This application provides a synopsis of the entire change history for a given function in the LibreOffice git repository.

Limitations:
The program is currently limited by the 4097 token limit of the GPT-3.5-turbo model.  Future improvements will need to be provided in order to bypass this restriction.
Certain change items don't contain bugzilla references, so those items are ignored.

Example Usage:
main.py UITools.cxx adjustBrowseBoxColumnWidth

Output:
{
  "role": "assistant",
  "content": "- On March 18, 2013, a bug report was created with an attached Perl script that contained examples of unnecessary ASCII art graphics in the source code. The bug report also included suggested easy hacks to remove certain comments and pointless class name declarations. 
  The script was provided to automate the cleanup process.\n\n- On April 8, 2013, Philipp Riemer committed a patch related to the bug. The patch was pushed to the \"master\" branch of the libreoffice/core repository. The patch was aimed at removing pointless comments and ASCII art in sw/source/core/doc. 
  The patch was expected to be included in the daily builds within the next 24-48 hours, and affected users were encouraged to test the fix and provide feedback.\n\n- On May 5, 2013, Philipp Riemer committed another patch related to the bug. 
  This patch was pushed to the \"master\" branch and targeted the removal of pointless comments and ASCII art in sw/source/core/draw. The patch was expected to be included in the daily builds within the next 24-48 hours, and affected users were encouraged to test the fix and provide feedback.
  \n\n- Also on May 5, 2013, Philipp Riemer committed another patch related to the bug. This patch was pushed to the \"master\" branch and focused on removing ASCII art in sw/source/core/graphic. The patch was expected to be included in the daily builds within the next 24-48 hours, 
  and affected users were encouraged to test the fix and provide feedback.\n\n- Lastly, on May 5, 2013, Philipp Riemer committed another patch related to the bug. This patch was pushed to the \"master\" branch and aimed to remove visual noise in sw/source/core/view. 
  The patch was expected to be included in the daily builds within the next 24-48 hours, and affected users were encouraged to test the fix and provide feedback.\n\nOverall, the bug reported on March 18, 2013, led to multiple patches being committed by Philipp Riemer to remove unnecessary comments, 
  ASCII art, and visual noise from different parts of the libreoffice/core source code. The fixes were gradually released in the daily builds for users to test and provide feedback."
}
