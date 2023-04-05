import { useState } from "react";

import Image from "next/image";
import { useRouter } from "next/router";

// lib
import { requiredAuth } from "lib/auth";
// services
import userService from "services/user.service";
// hooks
import useUser from "hooks/use-user";
// layouts
import DefaultLayout from "layouts/default-layout";
// components
import { InviteMembers, OnboardingCard, UserDetails, Workspace } from "components/onboarding";
// ui
import { PrimaryButton } from "components/ui";
// constant
import { ONBOARDING_CARDS } from "constants/workspace";
// images
import Logo from "public/onboarding/logo.svg";
// types
import type { NextPage, GetServerSidePropsContext } from "next";

const Onboarding: NextPage = () => {
  const [step, setStep] = useState(1);

  const [workspace, setWorkspace] = useState();

  const router = useRouter();

  const { user } = useUser();

  return (
    <DefaultLayout>
      <div className="grid h-full place-items-center p-5">
        {step <= 3 ? (
          <div className="w-full">
            <div className="text-center mb-8">
              <Image src={Logo} height="50" alt="Plane Logo" />
            </div>
            {step === 1 ? (
              <UserDetails user={user} setStep={setStep} />
            ) : step === 2 ? (
              <Workspace setStep={setStep} setWorkspace={setWorkspace} />
            ) : (
              <InviteMembers setStep={setStep} workspace={workspace} />
            )}
          </div>
        ) : (
          <div className="flex w-full max-w-2xl flex-col gap-12">
            <div className="flex flex-col items-center justify-center gap-7 rounded-[10px] bg-white px-14 py-10 text-center shadow-md">
              {step === 4 ? (
                <OnboardingCard data={ONBOARDING_CARDS.welcome} />
              ) : step === 5 ? (
                <OnboardingCard data={ONBOARDING_CARDS.issue} />
              ) : step === 6 ? (
                <OnboardingCard data={ONBOARDING_CARDS.cycle} />
              ) : step === 7 ? (
                <OnboardingCard data={ONBOARDING_CARDS.module} />
              ) : (
                <OnboardingCard data={ONBOARDING_CARDS.commandMenu} />
              )}
              <div className="mx-auto flex h-1/4 items-end lg:w-1/2">
                <PrimaryButton
                  type="button"
                  className="flex w-full items-center justify-center text-center "
                  size="md"
                  onClick={() => {
                    if (step === 8) {
                      userService
                        .updateUserOnBoard()
                        .then(() => {
                          router.push("/");
                        })
                        .catch((err) => {
                          console.log(err);
                        });
                    } else setStep((prevData) => prevData + 1);
                  }}
                >
                  {step === 4 || step === 8 ? "Get Started" : "Next"}
                </PrimaryButton>
              </div>
            </div>
          </div>
        )}
      </div>
    </DefaultLayout>
  );
};

// export const getServerSideProps = async (ctx: GetServerSidePropsContext) => {
//   const user = await requiredAuth(ctx.req?.headers.cookie);

//   const redirectAfterSignIn = ctx.resolvedUrl;

//   if (!user) {
//     return {
//       redirect: {
//         destination: `/signin?next=${redirectAfterSignIn}`,
//         permanent: false,
//       },
//     };
//   }

//   return {
//     props: {
//       user,
//     },
//   };
// };

export default Onboarding;