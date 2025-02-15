import { BlogMdxFrontmatter, getAllSecurityReports } from "@/lib/markdown";
import { formatDate2, stringToDate } from "@/lib/utils";
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Profzzor",
};

export default async function BlogIndexPage() {
  const blogs = (await getAllSecurityReports()).sort(
    (a, b) => stringToDate(b.date).getTime() - stringToDate(a.date).getTime()
  );
  return (
    <div className="w-full mx-auto flex flex-col gap-1 sm:min-h-[91vh] min-h-[88vh] pt-2">
      <div className="mb-7 flex flex-col gap-2">
        <h1 className="text-3xl font-extrabold">
          The latest Security Reports
        </h1>
        <p className="text-muted-foreground">
          All the latest Security Reports and News.
        </p>
      </div>
      <div className="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 sm:gap-8 gap-4 mb-5">
        {blogs.map((blog) => (
          <BlogCard {...blog} slug={blog.slug} key={blog.slug} />
        ))}
      </div>
    </div>
  );
}

function BlogCard({
  date,
  title,
  description,
  slug,
}: BlogMdxFrontmatter & { slug: string }) {
  return (
    <Link
      href={`/securityreports/${slug}`}
      className="flex flex-col gap-2 items-start border rounded-md py-5 px-3"
    >
      <h3 className="text-md font-semibold -mt-1 pr-7">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
      <div className="flex items-center justify-between w-full mt-auto">
        <p className="text-[13px] text-muted-foreground">
          Published on {formatDate2(date)}
        </p>
      </div>
    </Link>
  );
}