import { Typography } from "@/components/typography";
import { buttonVariants } from "@/components/ui/button";
import { getAllTechnicalArticlesStaticPaths, getTechnicalArticlesForSlug} from "@/lib/markdown";
import { ArrowLeftIcon } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";
import { formatDate } from "@/lib/utils";

type PageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata(props: PageProps) {
  const params = await props.params;

  const {
    slug
  } = params;

  const res = await getTechnicalArticlesForSlug(slug);
  if (!res) return null;
  const { frontmatter } = res;
  return {
    title: frontmatter.title,
    description: frontmatter.description,
  };
}

export async function generateStaticParams() {
  const val = await getAllTechnicalArticlesStaticPaths();
  if (!val) return [];
  return val.map((it) => ({ slug: it }));
}

export default async function BlogPage(props: PageProps) {
  const params = await props.params;

  const {
    slug
  } = params;

  const res = await getTechnicalArticlesForSlug(slug);
  if (!res) notFound();
  return (
    <div className="lg:w-[60%] sm:[95%] md:[75%] mx-auto">
      <Link
        className={buttonVariants({
          variant: "link",
          className: "!mx-0 !px-0 mb-7 !-ml-1 ",
        })}
        href="/technicalarticles"
      >
        <ArrowLeftIcon className="w-4 h-4 mr-1.5" /> Back to technicalarticles
      </Link>
      <div className="flex flex-col gap-3 pb-7 w-full mb-2">
        <p className="text-muted-foreground text-sm">
          {formatDate(res.frontmatter.date)}
        </p>
        <h1 className="sm:text-4xl text-3xl font-extrabold">
          {res.frontmatter.title}
        </h1>
      </div>
      <div className="!w-full">
        <Typography>{res.content}</Typography>
      </div>
    </div>
  );
}