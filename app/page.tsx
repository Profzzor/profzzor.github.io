export default function Home() {
  return (
    <div className="flex sm:min-h-[85.5vh] min-h-[85vh] flex-col items-center justify-center text-center px-2 sm:py-8 py-12">

      <p className="mb-5 sm:text-lg flex items-center gap-2 underline underline-offset-4 sm:-mt-12">About Me</p>
      <h1 className="text-3xl font-bold mb-4 sm:text-6xl">
      
      </h1>
      <p className="mb-8 sm:text-lg max-w-[800px] text-muted-foreground">
      A passionate Malware Analyst with a deep interest in threat intelligence and purple team methodologies.
      I specialize in detecting, analyzing, and defending against cyber threats, and 
      I’m constantly exploring new ways to stay one step ahead of evolving malware tactics.
      </p>
      <span className="flex flex-row items-start sm:gap-2 gap-0.5 text-muted-foreground text-md mt-7 -mb-12 max-[800px]:mb-12 font-code sm:text-base text-sm font-medium">
        {"@profzzor"}
      </span>
    </div>
  );
}
